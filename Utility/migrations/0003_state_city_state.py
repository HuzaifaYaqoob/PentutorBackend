# Generated by Django 4.0.5 on 2022-08-21 10:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Utility', '0002_auto_20211212_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=1000)),
                ('code', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='country_states', to='Utility.country')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_cities', to='Utility.state'),
        ),
    ]
