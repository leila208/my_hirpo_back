from rest_framework import serializers
from wizard.models import *
from django.http import JsonResponse
import pandas as pd

class HirponormsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hirponorms
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainSkill
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        

    
    
        
class DepartmentPositionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepartmentPosition
        fields = '__all__'
        
class ProjectDepartmentForCompSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDepartment
        fields = '__all__'
        
class ProjectDepartmentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProjectDepartment
        fields = ('name','employee_number')

#for comptencies
class ProjectDepartmentSerializer(serializers.ModelSerializer):
    departmentpositions = DepartmentPositionSerializer(many=True)
    compatencies = serializers.SerializerMethodField()
    allSkills = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDepartment
        fields = ('id', 'project', 'name', 'description', 'employee_number', 'departmentpositions','compatencies','allSkills')
        
    def get_compatencies(self,obj):
        return obj.get_compatencies()
    
    def get_allSkills(self,obj):
        return obj.get_allSkills()

class SimpleProjectDepartmentSerializer(serializers.ModelSerializer):
    compatencies = serializers.SerializerMethodField()
    class Meta:
        model = ProjectDepartment
        fields = '__all__'
        
    def get_compatencies(self,obj):
        df = pd.read_excel('media/Hirpolist.xlsx',usecols=['Department (eng)','Name of competency','Level (1-5)','Type (soft ot hard skills)','Position level'])
        df.fillna('null', inplace=True)
        df.rename(columns={'Level (1-5)': 'norm'}, inplace=True)
        df.rename(columns={'Department (eng)': 'department'}, inplace=True)
        df.rename(columns={'Name of competency': 'skill'}, inplace=True)
        df.rename(columns={'Type (soft ot hard skills)': 'skilltype'}, inplace=True)
        df.rename(columns={'Position level': 'position'}, inplace=True)
        data = df.to_dict(orient='records')
        comptency = []
        for x in data:
            for y in obj.departmentpositions.all():
                if x['department'] == obj.name and x['position']==y.name:
                    comptency.append(x)

        return comptency

class SkillNormSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()
    position = DepartmentPositionSerializer()
    class Meta:
        model = SkillNorm
        fields = '__all__'


class SkillNormUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillNorm
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    department = SimpleProjectDepartmentSerializer()
    position = DepartmentPositionSerializer()
    hard_goal = serializers.SerializerMethodField()
    soft_goal = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
    
    def get_soft_goal(self,obj):
        return obj.get_soft_goal()
    
    def get_hard_goal(self,obj):
        return obj.get_hard_goal()
    
    def get_goal(self,obj):
        return obj.get_goal()
    


