from rest_framework import generics
from rest_framework.views import APIView
from wizard.api.serializers import *
from rest_framework.response import Response
import os
import pandas as pd
import openpyxl
from wizard.models import *
from rest_framework.permissions import IsAuthenticated




#employee goal list
class UserListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserSerializer
    

class CreateProjectView(APIView):     
    def post(self,request,format=None):
        for pr in request.user.project.all():
            pr.delete()
        object_data = request.data.pop('inputValues')
        data=request.data
        
        data['companyLeader']=request.user.id
        project_serializer = ProjectSerializer(data=data)
        print(request.data,'-------------------------------')
        #datani listin icindeydi, object_data[0] seklinde yazilmisdi
        if project_serializer.is_valid(raise_exception=True):
            
            
            project = project_serializer.save()
            print(request.user,'-------------222-----------------')
            print(project,'------------------------------------')

            for item in list(object_data.keys()):
                name=str(item)
                value=str(object_data[item])

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
                    data = [{'name':'Specialist'},{'name':'Senior specialist'}]
                elif employee_number>3 and employee_number<6:
                    data = [{'name':'Junior-Assistant'},{'name':'Senior specialist'},{'name':'Manager'}]
                elif employee_number>5 and employee_number<11:
                    data = [{'name':'Junior-Assistant'},{'name':'Specialist'},{'name':'Senior specialist'},{'name':'Manager'}]   
                elif employee_number>10:
                    data = [{'name':'Junior-Assistant'},{'name':'Specialist'},{'name':'Senior specialist'},{'name':'Manager'},{'name':'Top manager'}]  
           
                for x in data:
                    position = DepartmentPositionSerializer(data=x)  
                    if position.is_valid(raise_exception=True):
                        position.save(department=department)
                #Department.objects.bulk_create()
                #bulk create daha uzun imis
        return Response({"message":"success","project":project_serializer.data.get('id')},status=201)
   
    #projectserializer.data.get('id') 55deki projectserializer.data['id'] idi check ele
        # partial = True arasdir   
"""{"companyleader": "111", "project_name": "ss", "industry": "IT", "employee_number": "22", "inputValues": {"Hr": "22"}}"""


#wizardpositionedit
class PositionUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        position_serializer = DepartmentPositionSerializer
        print(request.data,'----0-0-0-0-0-0-0-0-0-0-0data')
        data = request.data.get('selecteds')
        if data:
            for position_data in data:
                serializer = position_serializer(data=position_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
    
        data2 = request.data.get('objects2')
   
        if data2:
            for position_data in data2:
                position = DepartmentPosition.objects.get(id=position_data.get('id'))
                if position:            
                    position.delete()
        return Response(serializer.data)
    
    

        
#Department icinde comptenciler istifade olunmur
class SkillNormListView(generics.ListAPIView):
    serializer_class = ProjectDepartmentSerializer
    
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        data=self.kwargs['id']
        if data:
            project=Project.objects.get(id=data)
            ProjectDepartment.objects.filter(project=project)
            return queryset.filter(project=project)

#bir evvelki viewla eynidi check ele           
from rest_framework import status
class DepartmentPositionListView(generics.ListAPIView):
    serializer_class = ProjectDepartmentSerializer

    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        user=self.request.user
        if user.is_authenticated:
            project=Project.objects.get(companyLeader=user.id)
            return queryset.filter(project=project)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
class DepartmentForOrganizitialChart(generics.ListAPIView):
    serializer_class = DepartmentSerializerForOrganizitialChart
    
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        user=self.request.user
        if user.is_authenticated:
            project=Project.objects.get(companyLeader=user.id)
            return queryset.filter(project=project)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
                        
#wizardda go back ederken datanin silinmesi          
class go_back(APIView):
   def delete(self, request):
        data=request.data
        project = Project.objects.get(id=data.get("project"))
        project.delete()
        return Response({"message":"success"})
    
class project_delete(APIView):
   def delete(self, request):
        data=request.data
        user = User.objects.get(id=data.get("user_id"))
        employee = Employee.objects.get(user=user)
        projects = employee.project_set.all()
        for project in projects:
            project.delete()
        return Response({"message":"success"})
    
#excellden sqle
class OneTimeVieww(APIView):
    def post(self,request):
        df = pd.read_excel('media/Hirpolist.xlsx',usecols=['Department (eng)','Name of competency','Level (1-5)','Type (soft ot hard skills)','Position level'])
        df.fillna('null', inplace=True)
        df.rename(columns={'Level (1-5)': 'norm'}, inplace=True)
        df.rename(columns={'Department (eng)': 'department'}, inplace=True)
        df.rename(columns={'Name of competency': 'skill'}, inplace=True)
        df.rename(columns={'Type (soft ot hard skills)': 'skilltype'}, inplace=True)
        df.rename(columns={'Position level': 'position'}, inplace=True)

        data = df.to_dict(orient='records')
        print(data,'-lllllllllllllllllllllllllll')
        for x in data:     
            serializer =  HirponormsSerializer(data=x)
            serializer.is_valid(raise_exception=True)
            print(serializer,x)
            serializer.save()
        return Response({'message':'success'})
    
#after positions in wizard continue for creating norms
class OneTimeView(APIView):

    def post(self,*args,**kwargs):

        df = pd.read_excel('media/Hirpolist.xlsx',usecols=['Department (eng)','Name of competency','Level (1-5)','Type (soft ot hard skills)','Position level'])
        df.fillna('null', inplace=True)
        df.rename(columns={'Level (1-5)': 'norm'}, inplace=True)
        df.rename(columns={'Department (eng)': 'department'}, inplace=True)
        df.rename(columns={'Name of competency': 'skill'}, inplace=True)
        df.rename(columns={'Type (soft ot hard skills)': 'skilltype'}, inplace=True)
        df.rename(columns={'Position level': 'position'}, inplace=True)

        data = df.to_dict(orient='records')

        user = self.request.user.id
        

        if user:
            project=Project.objects.get(companyLeader=user)
            print(user,project)
        departments = ProjectDepartment.objects.filter(project=project)
        number = 0
        for x in departments:
            positions = DepartmentPosition.objects.filter(department=x.id)
            for item in data:
                for position in positions:
                    if item['position']==position.name and item['department']==position.department.name:

                        skill = SkillSerializer(data={'name':item['skill'],'position':position.id,'norm':item['norm'],'skilltype':item['skilltype']})
                       
                        skill.is_valid(raise_exception=True)
                        skill.save()
                        
                        number +=1
        return Response({"success":number})
    
    
#organizial chart department update
class DepartmentUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        
        department_serializer = SimpleProjectDepartmentSerializer
        removed = request.data.get('removedDepartments')
        added = request.data.get('editedDepartments')
        user=request.user
        project=Project.objects.get(companyLeader=user)
        for item in removed:
            dp = ProjectDepartment.objects.get(id=item.get('id'))
            if dp:
                dp.delete()
        for item in added:
            item["project"]=project.id
            serializer = department_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer)
        return Response({"message":"success"})

#wizardda comptency list view yaratmadan evvel       
class ExcellUploadView(generics.ListAPIView):
    serializer_class = SimpleProjectDepartmentSerializer

    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        data=self.request.user.id
        if data:
            project=Project.objects.get(companyLeader=data)
            return queryset.filter(project=project)
        
class WizardComptencySaveView(APIView):
    def post(self,request):
        data = request.data
        for comptency in data.get('createdNorms'):
            department = ProjectDepartment.objects.get(name=comptency['department'])
            position=DepartmentPosition.objects.get(name=comptency['position'],department=department)
            
            serializer = SkillNormCreateSerializer(data={'norm':comptency['newNorm'],"name":comptency['skill'],"position":position.id})
            
         
            serializer.is_valid(raise_exception=True)
            serializer.save()

        for comptency in data.get('editedNorms'):
            comp = MainSkill.objects.get(id=comptency['id'])
     
            serializer = SkillNormUpdateSerializer(comp,data={'norm':comptency['norm']})
            serializer.is_valid(raise_exception=True)
            serializer.save()

        for comptency in data.get('removedNorms'):
            myobj = MainSkill.objects.get(id=comptency)
            print(myobj)
            myobj.delete()
        return Response({'message':'delete success'})
            
class WeightUpdateView(APIView):     
     
    def put(self, request): 
        serializer = WeightUpdateSerializer   
        data=request.data
        for item in data:
            object = MainSkill.objects.get(id=item.get('id'))
            if object:
                myseria = serializer(object,data=item)
                myseria.is_valid(raise_exception=True)
                myseria.save()
        return Response({'message':'success'})

    
"""{  
    "id": 3,
    "norm": 3,
    "department": 1,
    "position": 73,
    "skill": 1
    }"""        
    
    
from django.contrib.auth.views import LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response

class LogoutAPIView(APIView):
    def post(self, request):

        # Call Django's LogoutView to log the user out
        logout_view = LogoutView.as_view()
        response = logout_view(request)
        
        # Return a success response
        return Response({'message': 'Logged out successfully'})
