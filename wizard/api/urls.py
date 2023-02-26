from django.urls import path
from wizard.api.views import *

app_name = "wizard-api"

urlpatterns = [
    path("employees/", UserListView.as_view(), name="List"),
    path("", CreateProjectView.as_view(), name="List"),

]