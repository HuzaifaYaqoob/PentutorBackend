# Generated by Django 3.2.4 on 2021-12-22 23:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Content', '0001_initial'),
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='cnic_number',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='home_tution',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='online_tutoring',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='per_hour',
            field=models.CharField(blank=True, default='', max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='time_end',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='time_start',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Tutor', 'Tutor'), ('Super-Admin', 'Super-Admin')], default='Student', max_length=20),
        ),
        migrations.CreateModel(
            name='SubjectToTeach',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('subject', models.CharField(default='', max_length=1000)),
                ('level', models.CharField(default='', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_subjects', to='Profile.teacherprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=600)),
                ('mobile', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='', max_length=100)),
                ('profession', models.CharField(default='', max_length=600)),
                ('relation', models.CharField(default='', max_length=600)),
                ('relation_time', models.CharField(default='', max_length=600)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_references', to='Profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=500)),
                ('year', models.CharField(default='', max_length=5)),
                ('institute', models.CharField(default='', max_length=500)),
                ('grade', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_qualifications', to='Profile.profile')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Content.subject')),
            ],
        ),
        migrations.CreateModel(
            name='PreferredDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
                ('sunday', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_preferred_days', to='Profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=100)),
                ('level', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='0', max_length=5, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_languages', to='Profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('slug', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(default='', max_length=600)),
                ('org_name', models.CharField(default='', max_length=1000)),
                ('from_date', models.DateField(blank=True, default=None)),
                ('to_date', models.DateField(blank=True, default=None)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_experiences', to='Profile.profile')),
            ],
        ),
    ]
