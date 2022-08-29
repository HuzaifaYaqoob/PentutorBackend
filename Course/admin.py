from django.contrib import admin
from .models import Course, CourseChapter, CourseMedia, CourseReview, ChapterVideo, CourseCategory


admin.site.register(Course)
admin.site.register(CourseChapter)
admin.site.register(CourseMedia)
admin.site.register(CourseReview)
admin.site.register(ChapterVideo)
admin.site.register(CourseCategory)