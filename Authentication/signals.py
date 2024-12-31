

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token
from Utility.models import Country, State


from Profile.models import StudentProfile, TeacherProfile


@receiver(post_save , sender = User)
def GenerateToken(sender, instance, created, **kwargs):
    user_types = {
        'tutor' : TeacherProfile,
        'student' : StudentProfile
    }
    if created:
        Token.objects.create(user = instance)
        new_profile = user_types[instance._type](
            user = instance,
            user_type = instance._type.capitalize(),
            name = instance.username
        )

        try:
            country = Country.objects.get(name__icontains = 'pakistan')
        except:
            country = Country.objects.all()[0]

        new_profile.Country = country
        new_profile.save()