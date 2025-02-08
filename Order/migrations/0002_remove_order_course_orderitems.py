# Generated by Django 4.0.5 on 2024-12-31 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0010_course_is_deleted'),
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='course',
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.course')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Order.order')),
            ],
        ),
    ]
