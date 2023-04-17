from django.urls import path
from wizard.api.views import *
from .views import *
app_name = "wizard-api"

urlpatterns = [
    path('ProjectsApiView/', ProjectsApiView.as_view(), name='ProjectsApiView'),
    path('AddPeriodApiView/', AddPeriodApiView.as_view(), name='AddPeriodApiView'),
    path('AddFrequencyApiView/', AddFrequencyApiView.as_view(), name='AddFrequencyApiView'),
    path('Frequencies/', Frequencies.as_view(), name='Frequencies'),
    
]