from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic

from main.views import DataMixin
from profiles.models import Profile
from .forms import RegisterForm, LogInForm


class UserRegisterView(DataMixin, generic.CreateView):
    template_name = 'users/registration_form.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy('login')


class UserLogInView(DataMixin, auth_views.LoginView):
    template_name = 'users/login_form.html'
    form_class = LogInForm

    def get_success_url(self):
        return reverse_lazy('catalog')


class UserLogOutView(DataMixin, auth_views.LogoutView):
    template_name = 'main/home.html'


class ProfileView(DataMixin, generic.DetailView):
    context_object_name = 'profile_detail'
    template_name = 'users/profile.html'
    model = Profile

    def get_queryset(self):
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
    template_name = 'users/change_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
    # если опять поломаются пользователи, то нужно делать что-то подобное
    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     return  self.model.objects.filter(user_id=pk)


class PasswordResetView(DataMixin, auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'


class PasswordResetDoneView(DataMixin, auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView(DataMixin, auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

    def get_success_url(self):
        return reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(DataMixin, auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
