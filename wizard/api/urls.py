from django.urls import path
from wizard.api.views import *

app_name = "wizard-api"

urlpatterns = [
    path("employees/", UserListView.as_view(), name="employees"),
    path("start", CreateProjectView.as_view(), name="start"),
    path("positionupdate/", PositionUpdateView.as_view(), name="positionupdate"),
    path("depposition/<id>", DepartmentPositionListView.as_view(), name="depposition"),
    path("compatencies/<id>", SkillNormListView.as_view(), name="competencies"),
    path("goback", Go_back.as_view(), name="go_back"),
    path('upload/<id>', ExcellUploadView.as_view(), name='upload_excel'),
    path('download/<id>', OneTimeView.as_view(), name='download_excel'),
    path("DepartmentUpdate/", DepartmentUpdateView.as_view(), name="DepartmentUpdate"),
    path("WizardComptencySaveView", WizardComptencySaveView.as_view(), name="WizardComptencySaveView"),
    path("weightUpdateView", WeightUpdateView.as_view(), name="WeightUpdateView"),
    path("project_delete", project_delete.as_view(), name="project_delete"),

]