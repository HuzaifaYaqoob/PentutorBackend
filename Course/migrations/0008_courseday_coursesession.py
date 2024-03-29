# Generated by Django 4.0.5 on 2022-09-13 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0016_alter_preferreddays_profile_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Course', '0007_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course_cart', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSession',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('session_type', models.CharField(blank=True, choices=[('OnCampus', 'On Campus'), ('Online', 'Online')], max_length=255, null=True)),
                ('duration', models.CharField(blank=True, choices=[('TwoMonths', 'Two Months'), ('FourMonths', 'Four Months'), ('FiveMonths', 'Five Months'), ('SixMonths', 'Six Months'), ('MoreSixMonths', 'More than Six Months')], max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course_cart', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursesession_course', to='Course.course')),
                ('course_days', models.ManyToManyField(blank=True, to='Course.courseday')),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.teacherprofile')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coursesession_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
