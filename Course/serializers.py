from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.conf import settings
from .models import Course, CourseCategory, CourseChapter, CourseMedia, CourseReview, ChapterVideo


class CourseMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMedia
        fields = ['slug', 'image']


class CourseSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    lectures = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    star_rating = serializers.SerializerMethodField()
    image_link = serializers.SerializerMethodField()
    
    def get_image_link(self, obj):
        try:
            media = CourseMedia.objects.get(course=obj).image
            return f"{settings.FRONT_END_URL}/{media}"
        except:
            media = None

    def get_media(self, obj):
        all_media = CourseMedia.objects.filter(course=obj)
        serialized = CourseMediaSerializer(all_media, many=True)
        return serialized.data
    
    def get_duration(self, obj):
        all_videos = list(ChapterVideo.objects.filter(course=obj).values_list('duration', flat=True))
        try:
            return str(sum(all_videos))
        except:
            return 'N/A'
        
    def get_lectures(self, obj):
        all_videos = list(ChapterVideo.objects.filter(course=obj).values_list('duration', flat=True))
        return len(all_videos)

    def get_students(self, obj):
        return 'N/A'

    def get_review_count(self, obj):
        all_reviews = CourseReview.objects.filter(course=obj)
        return len(all_reviews)

    def get_star_rating(self, obj):
        # all_reviews = CourseReview.objects.filter(course=obj)
        # return all_reviews.count()
        return 'N/A'

    class Meta:
        model = Course
        fields = [
            'user',
            'title',
            'short_title',
            'language',
            'course_category',
            'level',
            'price',
            'slug',
            'media',
            'duration',
            'lectures',
            'students',
            'review_count',
            'star_rating',
            'description',
            'image_link'
        ]
        
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
        

class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = '__all__'