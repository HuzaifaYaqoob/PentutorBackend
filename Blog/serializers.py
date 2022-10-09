

from django.conf import settings
from rest_framework import serializers

from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return f"{settings.BACKEND_URL}/media/{obj.image}"
        return None

    class Meta:
        model = BlogPost
        fields = '__all__'