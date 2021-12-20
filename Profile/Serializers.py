

from django.db.models import fields
from rest_framework import serializers
from .models import StudentProfile, TeacherProfile

from Authentication.serializers import UserSerializer
from Utility.serializers import CountrySerializer, CitySerializer


class StudentProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    Country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = StudentProfile
        fields = '__all__'



class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    Country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = TeacherProfile
        fields = '__all__'
