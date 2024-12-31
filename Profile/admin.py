from django.contrib import admin

from .models import StudentProfile, TeacherProfile, UserExperience, UserMedia, UserQualification, UserReferences, TutorProfessionalDetail, Language, PreferredDays
# Register your models here.


admin.site.register(StudentProfile)
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_editable = [
        'is_approved',
        'is_featured',
    ]
    list_display = [
        'name', 
        'slug', 
        'is_approved',
        'is_active',
        'is_deleted',
        'is_featured',
    ]


admin.site.register(UserQualification)
admin.site.register(UserExperience)
admin.site.register(UserReferences)
admin.site.register(UserMedia)
admin.site.register(TutorProfessionalDetail)
admin.site.register(Language)
admin.site.register(PreferredDays)