# Generated by Django 4.0.5 on 2022-08-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0006_userexperience'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='brith_place',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]