


from rest_framework import serializers

from .models import Course, CourseChapter, CourseMedia, CourseReview, ChapterVideo


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
            'category',
            'level',
            'price',
            'slug',
            'media',
            'duration',
            'lectures',
            'students',
            'review_count',
            'star_rating',
            'description'
        ]