

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token



@receiver(post_save , sender = User)
def GenerateToken(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user = instance)
