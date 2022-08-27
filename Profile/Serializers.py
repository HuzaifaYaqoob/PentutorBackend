

from django.db.models import fields
from rest_framework import serializers
from .models import PreferredDays, StudentProfile, SubjectToTeach, TeacherProfile, UserExperience, UserMedia, UserQualification, UserReferences, TutorProfessionalDetail, Language

from Authentication.serializers import UserSerializer
from Utility.serializers import CountrySerializer, CitySerializer, StateSerializer


class StudentProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    Country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = StudentProfile
        fields = '__all__'


class SubjectToTeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectToTeach
        fields = '__all__'

class TutorProfessionalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfessionalDetail
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
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

class PreferredDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferredDays
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
    days = serializers.SerializerMethodField()

    professional_details = serializers.SerializerMethodField()

    def get_professional_details(self, obj):
        data = dict()

        langs = Language.objects.filter(user=obj.user)
        serialized = LanguageSerializer(langs, many=True)
        data['languages'] = serialized.data


        pf_detail, created = TutorProfessionalDetail.objects.get_or_create(user=obj.user)

        p_ser = TutorProfessionalDetailSerializer(pf_detail)
        data.update(p_ser.data)

        subjcs = SubjectToTeach.objects.filter(user=obj.user)
        serialized = SubjectToTeachSerializer(subjcs, many=True)
        data['subjects'] = serialized.data

        return data

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

    def get_days(self, obj):
        day, created = PreferredDays.objects.get_or_create(profile=obj)
        print(' day ::: ' , day)
        serialized = PreferredDaysSerializer(day)
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
            'days',
            'professional_details',
            ]
