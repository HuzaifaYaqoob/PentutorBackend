

from django.contrib.auth.models import User
from rest_framework import fields, serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'auth_token']
        