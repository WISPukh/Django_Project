from django.contrib import messages
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView

from main.models import Order, OrderItem, Product
from .forms import CartAddProductForm, MakeOrderForm


class CartView(ListView):
    template_name = 'main/cart_detail.html'
    context_object_name = 'cart_items'
    model = OrderItem

    def get_queryset(self):
        self.queryset = self.annotate_total_product_price(user_pk=self.kwargs.get('pk'))
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.queryset:
            context.update(self.get_total_price())
        return context

    def annotate_total_product_price(self, user_pk):
        return (
            self.model.objects.filter(customer_id_id=user_pk, order_id__status='CART')
            .annotate(total_cost_per_item=F('quantity') * F('product_id__price'))
            .values(
                'quantity', 'product_id__name',
                'product_id__price', 'product_id_id',
                'total_cost_per_item', 'order_id__status'
            )
            .order_by('quantity')
        )

    def get_total_price(self):
        return self.queryset.aggregate(total_amount=Sum('total_cost_per_item'))


class AddCartItemView(CreateView):
    model = Order

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(request.POST)
        user_pk = request.session['_auth_user_id']
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

        return redirect('product_detail', product_pk)


class RemoveCartItemView(DeleteView):
    model = Order

    def delete(self, request, *args, **kwargs):
        user_pk = request.session['_auth_user_id']
        product_pk = self.kwargs.get('pk')

        deleted_product_quantity = OrderItem.objects.get(
            product_id_id=product_pk,
            customer_id_id=user_pk,
            order_id__status='CART'
        ).quantity
        OrderItem.objects.get(product_id_id=product_pk, customer_id_id=user_pk, order_id__status='CART').delete()

        instance = self.model.objects.get(product=product_pk, customer_id_id=user_pk, status='CART')
        self.model.objects.filter(product=product_pk, customer_id_id=user_pk, status='CART') \
            .update(quantity=F('quantity') - deleted_product_quantity)
        instance.product.remove(product_pk)

        if not instance.product.exists():
            self.model.objects.get(customer_id_id=user_pk, status='CART').delete()
        return redirect('cart_detail', user_pk)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class MakeOrderView(CreateView):
    form_class = MakeOrderForm
    template_name = 'main/make_order.html'
    model = OrderItem

    def get_queryset(self):
        user_pk = self.kwargs.get('pk')
        if Order.objects.filter(customer_id_id=user_pk, status='CART'):
            self.queryset = self.annotate_total_product_price(user_pk)
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.get_queryset()
        if self.queryset:
            context.update(self.get_total_price())
        return context

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

    def get_total_price(self):
        return self.get_queryset().aggregate(total_amount=Sum('total_cost_per_item'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        cleaned_data = self.get_form().data
        total_price = self.get_total_price()['total_amount']

        product_info = Product.objects.filter(
            orderitem__customer_id_id=user_pk, order__status='CART',
            order=Order.objects.get(customer_id_id=user_pk, status='CART')
        ).values('price', 'name', 'in_stock').order_by('in_stock').distinct()

        if self.amount_validation_error(user_pk, product_info):
            self.extra_context = messages.error(request, 'You chose more items than there is in stock')
            return redirect('make_order', user_pk)

        for item in product_info:
            self.model.objects.filter(customer_id_id=user_pk, order_id__status='CART').update(
                product_name=item['name'], unit_price=item['price'])

        Order.objects.filter(customer_id_id=user_pk, status='CART') \
            .update(city=cleaned_data['city'], address=cleaned_data['address'],
                    total_price=total_price, status='CR')
        return redirect('order_finished', user_pk)

    def amount_validation_error(self, user_pk, check_list):
        order_items_amount = self.model.objects.filter(customer_id_id=user_pk, order_id__status='CART').values(
            'quantity', 'product_name').order_by('quantity')

        for index in range(len(check_list)):
            # print(check_list[index]['in_stock'], '<', order_items_amount[index]['quantity'],
            #       check_list[index]['in_stock'] < order_items_amount[index]['quantity'])
            if check_list[index]['in_stock'] < order_items_amount[index]['quantity']:
                return True
        return False


class OrderDetailView(ListView):
    model = Order
    template_name = 'main/order_finished.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        return Order.objects.filter(customer_id_id=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        fucks_sake = self.model.objects.filter(customer_id_id=self.kwargs.get('pk')) \
            .prefetch_related('product__order_set__product') \
            .values(
            'product__price', 'product__name',
            'quantity', 'city',
            'address', 'status',
            'total_price'
        )
        print(fucks_sake)
        context['trash'] = fucks_sake
        for shit in context['order_items']:
            print(shit)
        print(context)
        return context
