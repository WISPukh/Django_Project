from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', UserRegister.as_view(), name='registration'),
    path('login/', UserLogIn.as_view(), name='login'),
    path('logout/', UserLogOut.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/change/', UserChangeProfileView.as_view(), name='change_profile'),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
