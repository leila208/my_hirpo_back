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
        print(request.data)
        project_serializer = ProjectSerializer(data=request.data)
        object_data = [request.data.get('inputValues')]
        if project_serializer.is_valid(raise_exception=True):
            project = project_serializer.save()
            print(object_data)
            for item in list(object_data[0].keys()):
                name=str(item)
                value=str(object_data[0][item])
                print(value,'s')
                
                last_data={"name":name,"employee_number":value}

                department_serializer = ProjectDepartmentUpdateSerializer(data=last_data)

                if department_serializer.is_valid(raise_exception=True):
                    department = department_serializer.save(project=project)

                if department.employee_number:
                    employee_number = department.employee_number
                else:
                    employee_number =1
                if employee_number == 1:
                    data=[{"name":"Senior"}]
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
        return Response({"message":"success","project":project_serializer.data['id']},status=201)
   
    
           
"""{"companyleader": "111", "project_name": "ss", "industry": "IT", "employee_number": "22", "inputValues": {"Hr": "22"}}"""

    
class PositionUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        position_serializer = DepartmentPositionSerializer
        print(request.data)
        data = request.data.get('selecteds')
        if data:
            for position_data in data:
                serializer = position_serializer(data=position_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        print(data,len(data),'deyisenler')
        data2 = request.data.get('objects2')
        print(data2,'silinenler')
        if data2:
            for position_data in data2:
                position = DepartmentPosition.objects.get(id=position_data.get('id'))
                if position:            
                    position.delete()
        return Response(serializer.data)
    
class CompatencyUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        compatency_serializer = SkillNormUpdateSerializer
        data = [request.data]
        for compatency_data in data:

            compatency = SkillNorm.objects.get(id=compatency_data.get('id'))
            serializer = compatency_serializer(compatency,data=compatency_data)
            print(serializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({"message":"success"})
    
"""{  
                "id": 3,
                "norm": 3,
                "department": 1,
                "position": 73,
                "skill": 1
            }"""        
        

class SkillNormListView(generics.ListAPIView):
    serializer_class = ProjectDepartmentSerializer
    
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        data=self.kwargs['id']
        if data:
            project=Project.objects.get(id=data)
            ProjectDepartment.objects.filter(project=project)
            return queryset.filter(project=project)

            
class DepartmentPositionListView(generics.ListAPIView):
    serializer_class = ProjectDepartmentSerializer

    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        data=self.kwargs['id']
        if data:
            project=Project.objects.get(id=data)
            return queryset.filter(project=project)
       

class Go_back(APIView):
   def delete(self, request):
        data=request.data
        project = Project.objects.get(id=data.get("project"))
        project.delete()
        return Response({"message":"success"})