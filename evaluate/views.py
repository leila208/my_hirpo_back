from rest_framework import generics
from rest_framework.views import APIView
from wizard.api.serializers import *
from rest_framework.response import Response
import os
import pandas as pd
import openpyxl
from wizard.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.views import LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

class ProjectsApiView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerr
    
    
    def get_queryset(self):

        data=self.request.user.id
        
        if data:
            project=Project.objects.filter(companyLeader=data)
            return project
        
class Frequencies(generics.ListAPIView):
    queryset = Evaluation_frequency.objects.all()
    serializer_class = Evaluation_frequencySerializer
    
    
    def get_queryset(self):
        queryset = Evaluation_frequency.objects.all()
        data=self.request.user.id
        
        if data:
            project=Project.objects.get(companyLeader=data)
            return queryset.filter(period__project_id = project.id)
class AddPeriodApiView(generics.CreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    
class AddFrequencyApiView(generics.CreateAPIView):
    queryset = Evaluation_frequency.objects.all()
    serializer_class = Evaluation_frequency