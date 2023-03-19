from rest_framework import serializers
from wizard.models import *
from django.http import JsonResponse

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
    
    class Meta:
        model = ProjectDepartment
        fields = '__all__'


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
    

class ExcelSerializer(serializers.Serializer):
    excel_file = serializers.FileField()
