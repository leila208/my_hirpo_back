from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = "accounts-api"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify/<id>", views.VerifyView.as_view(), name="verify"),
    path("SendResetCodeView/", views.SendResetCodeView.as_view(), name="SendResetCodeView"),
    path("ChangePasswordVerifyView/<id>", views.ChangePasswordVerifyView.as_view(), name="ChangePasswordVerifyView"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]