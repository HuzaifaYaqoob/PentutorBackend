# Generated by Django 4.0.5 on 2024-12-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoChat', '0008_alter_democallrequest_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='democallrequest',
            name='status',
            field=models.CharField(choices=[('Requested', 'Requested'), ('Accepted', 'Accepted')], default='Requested', max_length=30),
        ),
    ]
