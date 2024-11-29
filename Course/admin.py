from django.contrib import admin
from .models import CartItem, Course, CourseChapter, CourseDay, CourseMedia, CoursePurchase, CourseReview, ChapterVideo, CourseCategory, CourseSession


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_editable = ['is_deleted']
    list_filter = ['course_category', 'is_deleted']
    list_display = ['title', 'user', 'course_category', 'created_at', 'is_deleted',]

admin.site.register(CourseChapter)
admin.site.register(CourseMedia)
admin.site.register(CourseReview)
admin.site.register(ChapterVideo)
admin.site.register(CourseCategory)
admin.site.register(CartItem)
admin.site.register(CourseSession)
admin.site.register(CourseDay)
admin.site.register(CoursePurchase)