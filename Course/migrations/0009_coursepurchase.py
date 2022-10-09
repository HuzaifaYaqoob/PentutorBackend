# Generated by Django 4.0.5 on 2022-10-09 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Course', '0008_courseday_coursesession'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePurchase',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bought_courses', to='Course.course')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bought_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
