# Generated by Django 3.2.4 on 2021-12-22 23:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]