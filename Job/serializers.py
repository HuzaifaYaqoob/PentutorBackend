

from rest_framework import serializers
from .models import Job


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobGetMySerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super(JobGetAllSerializer, self).to_representation(instance)
        return data