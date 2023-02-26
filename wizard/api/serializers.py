from rest_framework import serializers
from wizard.models import *


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        
class ProjectDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectDepartment
        fields = '__all__'
    
    
        
class DepartmentPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepartmentPosition
        fields = '__all__'

class SkillNormSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    department = ProjectDepartmentSerializer()
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
    
