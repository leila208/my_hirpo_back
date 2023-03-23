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
        competencies = []
        for y in obj.departmentpositions.all():
            
            for norm in MainSkill.objects.filter(position=y,position__department__id=obj.id):
                competencies.append({'id':norm.id,'norm':norm.norm,'position':{'name':y.name,'id':y.id,'department':obj.id},'department':{'name':obj.name,'id':obj.id,'project':obj.project.id},'skill':{'name':norm.skill.name,'id':norm.skill.id,'department':norm.skill.position.department.id}})
        print(competencies)
        return competencies

class SkillNormSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()
    position = DepartmentPositionSerializer()
    class Meta:
        model = MainSkill
        fields = '__all__'


class SimpleSkillNormSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainSkill
        fields = '__all__'
    
    # def create(self, validated_data):
    #     position = validated_data.get('position')
    #     skill = validated_data.get('skill')
    #     old_object = SkillNorm.objects.filter(position=position, skill=skill)
    #     if old_object.exists():
    #         old_object.delete()
    #     new_object = SkillNorm.objects.create(**validated_data)
    #     return new_object

        


class SkillNormUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSkill
        fields = '__all__'
        
        

class UserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    department = SimpleProjectDepartmentSerializer()
    position = DepartmentPositionSerializer()
    hard_goal = serializers.SerializerMethodField()
    soft_goal = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
    
    def get_soft_goal(self,obj):
        return obj.get_soft_goal()
    
    def get_hard_goal(self,obj):
        return obj.get_hard_goal()
    
    def get_goal(self,obj):
        return obj.get_goal()
    


