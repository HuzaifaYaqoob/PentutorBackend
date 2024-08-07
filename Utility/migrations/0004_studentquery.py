# Generated by Django 4.0.5 on 2022-09-29 14:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Utility', '0003_state_city_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentQuery',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(default='', max_length=1000)),
                ('email', models.CharField(default='', max_length=1000)),
                ('mobile_number', models.CharField(default='', max_length=1000)),
                ('city', models.CharField(default='', max_length=1000)),
                ('area', models.CharField(default='', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
