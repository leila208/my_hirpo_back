from rest_framework import generics
from rest_framework.views import APIView
from wizard.api.serializers import *
from rest_framework.response import Response
from wizard.models import *

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateProjectView(APIView):
    
    def post(self,request,format=None):
        project_serializer = ProjectSerializer(data=request.data)
        object_data = request.data.get('objects')
        if project_serializer.is_valid(raise_exception=True):
            project = project_serializer.save()
            
            for obj_data in object_data:
                department_serializer = ProjectDepartmentSerializer(data=obj_data)

                if department_serializer.is_valid(raise_exception=True):
                    department = department_serializer.save(project=project)

                employee_number = department.employee_number
                if employee_number == 1:
                    data={"name":"Senior"}
                elif employee_number>1 and employee_number<4:
                    data = [{'name':'Senior'},{'name':'Senior Specialist'}]
                elif employee_number>3 and employee_number<6:
                    data = [{'name':'Manager'},{'name':'Senior Specialist'},{'name':'Junior'}]
                elif employee_number>5 and employee_number<11:
                    data = [{'name':'Manager'},{'name':'Senior Specialist'},{'name':'Junior'},{'name':'Seniior'}]   
                elif employee_number>10:
                    data = [{'name':'Top manager'},{'name':'Manager'},{'name':'Senior Specialist'},{'name':'Junior'},{'name':'Seniior'}]  

                for x in data:
                    position = DepartmentPositionSerializer(data=x)    
                    if position.is_valid(raise_exception=True):
                        position.save(department=department)
            
            return Response({'message':"success"})
        return Response({'error':department.errors + project_serializer.errors+position.errors})  
    
    
    
    
    
"""{"companyleader": 110, "project_name": "TEST","employee_number": 25, "industry": "IT", "objects": [{"name": "TEST","employee_number":3},{"name": "TEWST","employee_number":3},{"name": "TESTT","employee_number":3}]}"""
