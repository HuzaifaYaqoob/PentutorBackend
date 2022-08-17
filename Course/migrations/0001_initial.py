# Generated by Django 4.0.5 on 2022-08-17 01:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(default='', max_length=500)),
                ('short_title', models.CharField(default='', max_length=300)),
                ('language', models.CharField(default='', max_length=100)),
                ('category', models.CharField(default='', max_length=200)),
                ('level', models.CharField(default='', max_length=200)),
                ('price', models.PositiveIntegerField(default=0)),
                ('discount_price', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(default='')),
                ('things_you_will_learn', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseMedia',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(upload_to='course/images/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_medias', to='Course.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseChapter',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(default='', max_length=500)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_chapters', to='Course.course')),
            ],
        ),
        migrations.CreateModel(
            name='ChapterVideo',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('video', models.FileField(upload_to='courses/chapter/videos/')),
                ('vid_thumbnail', models.ImageField(upload_to='course/chapter/video_thumbnails/')),
                ('duration', models.CharField(default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapter_videos', to='Course.coursechapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_videos', to='Course.course')),
            ],
        ),
    ]
