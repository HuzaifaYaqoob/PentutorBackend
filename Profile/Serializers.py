

from django.db.models import fields
from rest_framework import serializers
from .models import StudentProfile, TeacherProfile, UserExperience, UserMedia, UserQualification, UserReferences

from Authentication.serializers import UserSerializer
from Utility.serializers import CountrySerializer, CitySerializer, StateSerializer


class StudentProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    Country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = StudentProfile
        fields = '__all__'


class UserQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQualification
        fields = '__all__'

class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = '__all__'

class UserReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReferences
        fields = '__all__'


class UserMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedia
        fields = '__all__'


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    Country = CountrySerializer()
    state = StateSerializer()
    city = CitySerializer()

    qualifications = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    references = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    def get_qualifications(self, obj):
        all_qualifications = UserQualification.objects.filter(user=obj.user)
        serialized = UserQualificationSerializer(all_qualifications, many=True)
        return serialized.data


    def get_experiences(self, obj):
        all_experiences = UserExperience.objects.filter(user=obj.user)
        serialized = UserExperienceSerializer(all_experiences, many=True)
        return serialized.data

    def get_references(self, obj):
        all_references = UserReferences.objects.filter(user=obj.user)
        serialized = UserReferencesSerializer(all_references, many=True)
        return serialized.data

    def get_videos(self, obj):
        all_videos = UserMedia.objects.filter(user=obj.user)
        serialized = UserMediaSerializer(all_videos, many=True)
        return serialized.data


    class Meta:
        model = TeacherProfile
        fields = [
            'user',
            'name',
            'user_type',
            'mobile',
            'Country',
            'state',
            'city',
            'area',
            'date_of_birth',
            'brith_place',
            'gender',
            'detail',
            'qualifications',
            'experiences',
            'references',
            'videos',
            'profile_image',
            'degree_image',
            'cnic_image',
            'cnic_back',
            'cnic_number',
            'slug',
            'home_tution',
            'online_tutoring',
            'per_hour',
            'time_start',
            'time_end',
            ]
