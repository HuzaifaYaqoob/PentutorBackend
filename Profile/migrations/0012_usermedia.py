# Generated by Django 4.0.5 on 2022-08-21 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0011_userreferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMedia',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('video', models.FileField(upload_to='tutor_videos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_medias', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
