from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from profiles.models import Profile

from .forms import *

from .models import *

menu = [
    {'title': 'Главная', 'url': 'index', 'img_url': 'img/home.png'},
    {'title': 'О компании', 'url': 'about', 'img_url': 'img/about.png'},
    {'title': 'Каталог товаров', 'url': 'catalog', 'img_url': 'img/catalog.png'},
    {'title': 'Отзывы', 'url': 'reviews', 'img_url': 'img/review.png'},
]


def index(request):
    return render(request, 'main/home.html', {'menu': menu})


def about(request):
    return render(request, 'main/about.html', {'menu': menu})


def reviews(request):
    return render(request, 'main/reviews.html', {'menu': menu})


class DataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class CatalogView(DataMixin, generic.ListView):
    model = Category
    ordering = 'id'
    template_name = 'main/catalog.html'
    context_object_name = 'catalog_list'


class ProductByCategoryView(DataMixin, generic.ListView):
    model = Product
    context_object_name = 'products_list'
    template_name = 'main/products_by_category.html'

    def get_queryset(self):
        return Product.objects.filter(category__name=self.kwargs.get('category_name'))


class ProductDetailView(DataMixin, generic.DetailView):
    context_object_name = 'product_detail'
    template_name = 'main/product_detail.html'

    def get_queryset(self):
        current_item = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        # current_item = Product.objects.get(pk=self.kwargs.get('pk'))
        # print(ContentType.model_class(current_item.content_type))
        content_type = ContentType.model_class(current_item.content_type)
        return content_type.objects.all()


class UserRegister(DataMixin, generic.CreateView):
    template_name = 'main/registration_form.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy('login')


class UserLogIn(DataMixin, auth_views.LoginView):
    template_name = 'main/login_form.html'
    form_class = LogInForm

    def get_success_url(self):
        return reverse_lazy('catalog')


class UserLogOut(DataMixin, auth_views.LogoutView):
    template_name = 'main/home.html'


class ProfileView(DataMixin, generic.DetailView):
    context_object_name = 'profile_detail'
    template_name = 'main/profile.html'
    model = Profile

    def get_queryset(self):
        # TODO: вывод для несовпадающих profile_id и user_id поломан. для остальных норм
        return self.model.objects.filter(user=self.kwargs.get('pk'))


class UserChangeProfileView(DataMixin, generic.UpdateView):
    model = Profile
    fields = [
        'bio',
        'birthday',
        'phone',
        'age',
        'region'
    ]
    template_name = 'main/change_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     print(pk)
    #     obj = self.model.objects.filter(user_id=pk)
    #     return obj
    # def get_object(self, queryset=None):

    #     return obj


# class MyPasswordChangeView(DataMixin, auth_views.PasswordChangeView):
#     template_name = 'main/password-reset.html'
#     # form_class = PasswordChange
#     # success_url = reverse_lazy('login')


# class CustomPasswordResetView(DataMixin, auth_views.PasswordResetView):
#     template_name = 'main/password_reset.html'


class MyPasswordResetView(DataMixin, auth_views.PasswordResetView):
    # email_template_name = 'password_reset_email_my.html'
    template_name = 'main/password_reset.html'


class MyPasswordResetDone(DataMixin, auth_views.PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class MyPasswordResetConfirmView(DataMixin, auth_views.PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'

    def get_success_url(self):
        return reverse_lazy('password_reset_complete')


class MyPasswordResetCompleteView(DataMixin, auth_views.PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'
