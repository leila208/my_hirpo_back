from django.urls import path
from wizard.api.views import *

app_name = "wizard-api"

urlpatterns = [
    path("employees/", UserListView.as_view(), name="employees"),
    path("start", CreateProjectView.as_view(), name="start"),
    path("positionupdate", PositionUpdateView.as_view(), name="positionupdate"),
    path("depposition/<id>", DepartmentPositionListView.as_view(), name="depposition"),
    path("compatencies/<id>", SkillNormListView.as_view(), name="competencies"),
    path("compatencyupdate", CompatencyUpdateView.as_view(), name="competencyupdate"),
    path("goback", Go_back.as_view(), name="go_back"),

]