from django.contrib import admin
from .models import CartItem, Course, CourseChapter, CourseDay, CourseMedia, CourseReview, ChapterVideo, CourseCategory, CourseSession


admin.site.register(Course)
admin.site.register(CourseChapter)
admin.site.register(CourseMedia)
admin.site.register(CourseReview)
admin.site.register(ChapterVideo)
admin.site.register(CourseCategory)
admin.site.register(CartItem)
admin.site.register(CourseSession)
admin.site.register(CourseDay)