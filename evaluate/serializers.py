from rest_framework import serializers
from account.models import *
from wizard.models import *
from django.http import JsonResponse


class Evaluation_frequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation_frequency
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    frequency = Evaluation_frequencySerializer(many=True)
    class Meta:
        model = Period
        fields = '__all__'
        
class ProjectSerializerr(serializers.ModelSerializer):
    period = PeriodSerializer(many=True)
    
    
    class Meta:
        model = Project
        fields = '__all__'
        
        
        