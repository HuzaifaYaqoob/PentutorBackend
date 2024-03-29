# Generated by Django 4.0.5 on 2022-09-02 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Course', '0005_chaptervideo_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursereview',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coursereview',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coursereview',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coursereview_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='coursereview',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursereview_course', to='Course.course'),
        ),
        migrations.AlterField(
            model_name='coursereview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
