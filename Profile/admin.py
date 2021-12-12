from django.contrib import admin

from .models import StudentProfile, TeacherProfile
# Register your models here.


admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)