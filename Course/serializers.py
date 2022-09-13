from rest_framework import serializers
from django.conf import settings
from .models import CartItem, Course, CourseCategory, CourseChapter, CourseDay, CourseMedia, CourseReview, ChapterVideo, CourseSession


class CourseMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMedia
        fields = ['slug', 'image']


        
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
        
        
class ChapterVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    vid_thumbnail = serializers.SerializerMethodField()
    
    def get_video(self, obj):
        if obj.video:
            return f"{settings.FRONT_END_URL}/{obj.video}"
        else:
            return None
        
    def get_vid_thumbnail(self, obj):
        if obj.vid_thumbnail:
            return f"{settings.FRONT_END_URL}/{obj.vid_thumbnail}"
        else:
            return None

    class Meta:
        model = ChapterVideo
        fields = ['course', 'title', 'chapter', 'video', 'vid_thumbnail', 'duration', 'slug', 'created_at']


class CourseMediaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj):
        if obj.image:
            return f"{settings.FRONT_END_URL}/{obj.image}"
        else:
            return None

    class Meta:
        model = CourseMedia
        fields = ['course', 'image', 'slug', 'created_at']
        

class CourseChapterSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    
    def get_video(self, obj):
        video = ChapterVideo.objects.filter(chapter=obj)
        serializer = ChapterVideoSerializer(video, many=True).data
        return serializer
    class Meta:
        model = CourseChapter
        fields = ['title', 'course', 'slug', 'created_at', 'video']


class CourseSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    lectures = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    star_rating = serializers.SerializerMethodField()
    chapter = serializers.SerializerMethodField()
    
    
    def get_chapter(self, obj):
        chapters = CourseChapter.objects.filter(course=obj)
        serializer = CourseChapterSerializer(chapters, many=True).data
        return serializer
    
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
            'chapter'
        ]
        
class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
    
class CourseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSession
        fields = ['slug', 'title', 'instructor', 'course', 'user','start_date',
            'end_date', 'start_time', 'end_time', 'session_type',
            'duration', 'created_at'
        ]

class CourseDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDay
        fields = '__all__'

class GetCourseSessionSerializer(serializers.ModelSerializer):
    course_days = CourseDaySerializer(many=True)
    
    class Meta:
        model = CourseSession
        fields = [
            'slug', 'title', 'instructor', 'course', 'user','start_date',
            'end_date', 'start_time', 'end_time', 'session_type',
            'duration', 'created_at', 'course_days'
        ]
        
        