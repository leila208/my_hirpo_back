from rest_framework import serializers
from account.models import *
from wizard.models import *
from django.http import JsonResponse

class PerioddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = '__all__'

class Evaluation_ffrequencySerializer(serializers.ModelSerializer):
    freq_number = serializers.IntegerField()
    period = PerioddSerializer()
    class Meta:
        model = Evaluation_frequency
        fields = '__all__'
        
class Evaluation_frequencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Evaluation_frequency
        fields = '__all__'
        
class MainSkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MainSkill
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    frequency = Evaluation_frequencySerializer(many=True)
    position_count = serializers.SerializerMethodField()
    class Meta:
        model = Period
        fields = '__all__'
        
    def get_position_count(self,obj):
        count = 0
        a = obj.project
        for x in a.departments.all():
            for y in x.departmentpositions.all():
                count += 1
        return count
        
    
        
class ProjectSerializerr(serializers.ModelSerializer):
    
    period = PeriodSerializer(many=True)
    class Meta:
        model = Project
        fields = '__all__'
    
class AllScoresSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllScores
        fields = '__all__'
    
class UserSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkill
        fields = '__all__'
            
        
class SimpleProjectDepartmentSerializer(serializers.ModelSerializer):
    compatencies = serializers.SerializerMethodField()
    get_allSkills = serializers.SerializerMethodField()
    class Meta:
        model = ProjectDepartment
        fields = '__all__'
    
        
    def get_compatencies(self,obj):
        competencies = []
        for y in obj.departmentpositions.all():
            
            for norm in MainSkill.objects.filter(position=y,position__department__id=obj.id):
                competencies.append({'id':norm.id,'weight':norm.weight,'norm':norm.norm,'position':{'name':y.name,'id':y.id,'department':obj.id},'department':{'name':obj.name,'id':obj.id,'project':obj.project.id},'skill':{'name':norm.name,'id':norm.id,'department':norm.position.department.id}})
        print(competencies)
        return competencies
    
    def get_get_allSkills(self,obj):
        return obj.get_allSkills()
    
class employeeSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    class Meta:
        model = Employee
        fields = '__all__'
        
    def get_total_score(self,obj):
        return obj.get_total_score()
    
        
        

        
        
        