from django.contrib import admin

from .models import StudentProfile, TeacherProfile, UserExperience, UserMedia, UserQualification, UserReferences
# Register your models here.


admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(UserQualification)
admin.site.register(UserExperience)
admin.site.register(UserReferences)
admin.site.register(UserMedia)