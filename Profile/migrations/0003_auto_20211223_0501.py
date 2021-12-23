# Generated by Django 3.2.4 on 2021-12-23 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_auto_20211223_0459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherprofile',
            name='cnic_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='cnic_back',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/cnic_images/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='cnic_number',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
    ]