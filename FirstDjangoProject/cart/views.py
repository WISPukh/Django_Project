from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView

from main.models import Order, OrderItem, Product
from .forms import CartAddProductForm, MakeOrderForm
from .tasks import order_created


class OrderAmountExceededError(Exception):
    pass


class CartDataMixin:
    model = OrderItem

    def annotate_total_product_price(self, user_pk):
        return (
            self.model.objects.filter(customer_id_id=user_pk, order_id__status='CART')
            .annotate(total_cost_per_item=F('quantity') * F('product_id__price'))
            .values(
                'quantity', 'product_id__name',
                'product_id__price', 'product_id_id',
                'total_cost_per_item'
            )
            .order_by('quantity')
        )


class CartView(LoginRequiredMixin, CartDataMixin, ListView):
    template_name = 'cart/cart_detail.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        self.queryset = self.annotate_total_product_price(user_pk=self.request.user.pk)
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.queryset:
            context.update(self.get_total_price())
        return context

    def get_total_price(self):
        return self.queryset.aggregate(total_amount=Sum('total_cost_per_item'))


class AddCartItemView(LoginRequiredMixin, CreateView):
    model = Order

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(request.POST)
        user_pk = self.request.user.pk
        product_pk = self.kwargs.get('pk')
        quantity = form.data['quantity']

        order_item, created_order_item = self.model.objects.get_or_create(
            customer_id_id=user_pk,
            status='CART'
        )
        order_item.product.add(product_pk)

        snapshot_item, created_snap_item = OrderItem.objects.get_or_create(
            customer_id_id=user_pk,
            product_id=Product.objects.get(pk=product_pk),
            order_id=order_item
        )

        if created_order_item and created_snap_item:
            order_item.quantity = quantity
            snapshot_item.quantity = quantity
        else:
            order_item.quantity = F('quantity') + quantity
            snapshot_item.quantity = F('quantity') + quantity
        snapshot_item.save()
        order_item.save()
        messages.success(request, "You've successfully added product to cart!")
        return redirect('product_detail', product_pk)


class RemoveCartItemView(LoginRequiredMixin, DeleteView):
    model = Order

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        user_pk = self.request.user.pk
        product_pk = self.kwargs.get('pk')

        deleted_product_quantity = OrderItem.objects.get(
            product_id_id=product_pk,
            customer_id_id=user_pk,
            order_id__status='CART'
        ).quantity
        OrderItem.objects.get(product_id_id=product_pk, customer_id_id=user_pk, order_id__status='CART').delete()

        instance = self.model.objects.get(product=product_pk, customer_id_id=user_pk, status='CART')
        self.model.objects.filter(
            product=product_pk,
            customer_id_id=user_pk,
            status='CART'
        ).update(quantity=F('quantity') - deleted_product_quantity)
        instance.product.remove(product_pk)

        if not instance.product.exists():
            self.model.objects.get(customer_id_id=user_pk, status='CART').delete()
        return redirect('cart_detail')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class MakeOrderView(LoginRequiredMixin, CartDataMixin, CreateView):
    form_class = MakeOrderForm
    template_name = 'cart/make_order.html'

    def get_queryset(self):
        user_pk = self.request.user.pk
        if Order.objects.filter(customer_id_id=user_pk, status='CART'):
            self.queryset = self.annotate_total_product_price(user_pk)
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.get_queryset()
        if self.queryset:
            context.update(self.get_total_price())
        return context

    def get_total_price(self):
        return self.get_queryset().aggregate(total_amount=Sum('total_cost_per_item'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_pk = self.request.user.pk
        cleaned_data = self.get_form().data
        total_price = self.get_total_price()['total_amount']

        order_items = self.model.objects.filter(customer_id_id=user_pk, order_id__status='CART').order_by(
            'product_id_id')

        cart_products = Product.objects.filter(
            orderitem__customer_id_id=user_pk,
            order__status='CART',
            order=Order.objects.get(customer_id_id=user_pk, status='CART')
        ).distinct().order_by('pk')

        try:
            self.validate_cart_products_amount(cart_products, order_items)
        except OrderAmountExceededError:
            messages.error(request, 'You chose more items than there is in stock or you chose less than 1 product')
            return redirect('make_order')

        for item in order_items:
            item.product_name = item.product_id.name
            item.unit_price = item.product_id.price
        self.model.objects.bulk_update(order_items, ['product_name', 'unit_price'])

        order = Order.objects.get(customer_id_id=user_pk, status='CART')

        self.decrease_in_stock_amount(cart_products, order_items)

        order.city = cleaned_data['city']
        order.address = cleaned_data['address']
        order.total_price = total_price
        order.status = 'CR'
        order.save()
        order_created.delay(order.pk)

        return redirect('orders')

    @staticmethod
    def validate_cart_products_amount(check_list, order_items):
        for index, item in enumerate(check_list):
            if item.in_stock < order_items[index].quantity:
                raise OrderAmountExceededError
            if 1 > order_items[index].quantity:
                raise OrderAmountExceededError
        return None

    @staticmethod
    def decrease_in_stock_amount(product_info, order_items):
        """
        Subtract from stock amount of products in user's order
        """

        for index, product in enumerate(product_info):
            product.in_stock -= order_items[index].quantity
        Product.objects.bulk_update(product_info, ['in_stock'])


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'cart/order_finished.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer_id_id=self.request.user.pk, status='CR').values(
            'id',
            'total_price',
            'quantity',
            'city',
            'address'
        ).order_by('pk')

    def get_total_price(self):
        return self.queryset.aggregate(total_amount=Sum('total_cost_per_item'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for order in context['orders']:
            order_item = OrderItem.objects.filter(
                customer_id_id=self.request.user.pk,
                order_id__status='CR',
                order_id_id=order['id']
            ).annotate(total_cost_per_item=F('quantity') * F('product_id__price')).values(
                'quantity',
                'product_name',
                'product_id__price',
                'total_cost_per_item'
            )
            order['items'] = order_item
        return context
