from django.urls import path
from . import views

app_name = "accounts-api"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify/<id>", views.VerifyView.as_view(), name="verify"),
    path("SendResetCodeView/", views.SendResetCodeView.as_view(), name="SendResetCodeView"),
    path("ChangePasswordVerifyView/<id>", views.ChangePasswordVerifyView.as_view(), name="ChangePasswordVerifyView"),
]