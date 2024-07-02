from django.contrib import admin

from .models import StudentProfile, TeacherProfile, UserExperience, UserMedia, UserQualification, UserReferences, TutorProfessionalDetail, Language, PreferredDays
# Register your models here.


admin.site.register(StudentProfile)
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['name' , 'slug']


admin.site.register(UserQualification)
admin.site.register(UserExperience)
admin.site.register(UserReferences)
admin.site.register(UserMedia)
admin.site.register(TutorProfessionalDetail)
admin.site.register(Language)
admin.site.register(PreferredDays)