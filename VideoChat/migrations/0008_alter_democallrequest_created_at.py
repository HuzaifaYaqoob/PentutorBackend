# Generated by Django 4.0.5 on 2024-12-10 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoChat', '0007_alter_videochat_paticipants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='democallrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
