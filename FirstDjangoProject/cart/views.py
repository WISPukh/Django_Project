from django.db import transaction
from django.db.models import F, Sum, ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView

from main.models import Order, Product
from .forms import CartAddProductForm, MakeOrderForm


# def order_finished(request):
#     return render(request, 'main/order_finished.html')


class CartView(ListView):
    template_name = 'main/cart_detail.html'
    context_object_name = 'cart_items'
    model = Order

    # на уровне Python
    # def get_queryset(self):
    #     return Cart.objects.filter(customer_id_id=self.kwargs.get('pk')).prefetch_related('customer_id_id').values(
    #         'product_id__name', 'product_id__price', 'quantity', 'product_id_id')
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     for product in context['cart_items']:
    #         product['total_product_price'] = product['product_id__price'] * product['quantity']
    #
    #     context['total'] = {
    #         'total_cart_price': sum([product['total_product_price'] for product in context['cart_items']])
    #     }
    #     return context

    # на SQL
    def get_queryset(self):
        self.queryset = self.annotate_total_product_price(user_pk=self.kwargs.get('pk'))
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_total_price())
        return context

    def annotate_total_product_price(self, user_pk):
        return (
            self.model.objects.filter(customer_id_id=user_pk)
            .annotate(total_cost_per_item=F('product__order__quantity') * F('product__price'))
            .values(
                'product__price', 'product__name', 'product',
                'product__order__quantity', 'total_cost_per_item', 'customer_id_id'
            )
            .order_by('quantity')
        )

    def get_total_price(self):
        return self.queryset.aggregate(total_amount=Sum('total_cost_per_item'))


class AddCartItemView(CreateView):
    model = Order

    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(request.POST)
        user_pk = request.session['_auth_user_id']
        product_pk = self.kwargs.get('pk')
        quantity = form.data['quantity']

        order_item, created_order_item = self.model.objects.get_or_create(
            customer_id_id=user_pk,
        )
        order_item.product.add(product_pk)
        if created_order_item:
            order_item.quantity = quantity
        else:
            order_item.quantity = F('quantity') + quantity
        order_item.save()
        return redirect('product_detail', product_pk)


class RemoveCartItemView(DeleteView):
    model = Order

    def delete(self, request, *args, **kwargs):
        user_pk = request.session['_auth_user_id']
        product_pk = self.kwargs.get('pk')
        instance = self.model.objects.get(product=product_pk, customer_id_id=user_pk)
        instance.product.remove(product_pk)
        if not instance.product.exists():
            self.model.objects.get(customer_id_id=user_pk).delete()
        return redirect('cart_detail', user_pk)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class MakeOrderView(CreateView):
    form_class = MakeOrderForm
    template_name = 'main/make_order.html'

    def get_queryset(self):
        self.queryset = self.annotate_total_product_price(user_pk=self.kwargs.get('pk'))
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.get_queryset()
        context.update(self.get_total_price())
        return context

    def annotate_total_product_price(self, user_pk):
        return (
            Order.objects.filter(customer_id_id=user_pk)
            .annotate(total_cost_per_item=F('quantity') * F('product__price'))
            .values(
                'product__price', 'product__name',
                'quantity', 'product', 'total_cost_per_item'
            )
            .order_by('quantity')
        )

    def get_total_price(self):
        return self.get_queryset().aggregate(total_amount=Sum('total_cost_per_item'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_pk = self.request.session['_auth_user_id']
        form = self.get_form()
        cleaned_data = form.data
        total_price = self.get_total_price()['total_amount']
        products_info = self.get_queryset()
        print(products_info)
        products = Order.objects.filter(customer_id_id=self.kwargs.get('pk')).prefetch_related('prod')
        # products_m2m = Product.objects.filter(pk=products_info[])
        # instance = Order.objects.create(total_price=total_price, customer_id_id=user_pk,
        #                                 address=cleaned_data['address'], quantity=products_info['quantity'],
        #                                 city=cleaned_data['city'])
        # instance.product.set()
        # Cart.objects.filter(customer_id_id=user_pk).delete()
        return redirect('order_finished', user_pk)


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
            .values('product__price', 'product__name',
                    'quantity', 'city',
                    'address', 'status',
                    'total_price')
        print(fucks_sake)
        for shit in context['order_items']:
            print(shit)
        context['trash'] = fucks_sake
        print(context)
        return context
