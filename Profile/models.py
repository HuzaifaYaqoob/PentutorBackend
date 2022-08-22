from django.db import models
import uuid
from django.db.models import base
from django.utils.timezone import now

from django.contrib.auth.models import User
from Utility.models import Country, City, State
from Content.models import Subject

# Create your models here.


class PreferredDays(models.Model):
    profile = models.ForeignKey('Profile' , on_delete=models.CASCADE , default=None, blank=True, related_name='profile_preferred_days')

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    

class SubjectToTeach(models.Model):
    profile = models.ForeignKey('TeacherProfile' , on_delete=models.CASCADE , default=None, blank=True, related_name='teacher_subjects')

    subject = models.CharField(max_length=1000 , default='')
    level = models.CharField(max_length=1000 , default='')

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)


class Language(models.Model):

    LANGUAGE_LEVELCHOICES = [
        ('0' , '0'),
        ('1' , '1'),
        ('2' , '2'),
        ('3' , '3'),
        ('4' , '4'),
        ('5' , '5'),
    ]

    profile = models.ForeignKey('Profile' , on_delete=models.CASCADE , default=None, blank=True, related_name='profile_languages')

    name = models.CharField(max_length=100, default='')
    level = models.CharField(choices=LANGUAGE_LEVELCHOICES , max_length=5 , default='0', blank=True , null=True)

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)



class Profile(models.Model):

    TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Tutor', 'Tutor'),
        ('Super-Admin', 'Super-Admin'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),

    ]

    user = models.OneToOneField( User, on_delete=models.DO_NOTHING, blank=True, related_name='user_profile')
    name = models.CharField(max_length=200, default='')
    user_type = models.CharField(choices=TYPE_CHOICES, default='Student', max_length=20)

    mobile = models.CharField(max_length=22, null=True, blank=True, default='')

    Country = models.ForeignKey(Country , on_delete=models.SET_NULL , null=True ,  blank=True )
    state = models.ForeignKey(State , on_delete=models.SET_NULL , null=True ,  blank=True )
    city = models.ForeignKey(City , on_delete=models.SET_NULL , null=True ,  blank=True )
    area = models.CharField(max_length=500, default='')
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    brith_place = models.CharField(default='', blank=True, null=True, max_length=1000)
    nationality = models.CharField(default='', blank=True, null=True, max_length=1000)
    gender = models.CharField(choices=GENDER_CHOICES, default='Male', max_length=10)
    detail = models.TextField(default='')
    qualification = models.CharField(max_length=200, default='')

    profile_image = models.ImageField(upload_to='images/profile_images/')
    degree_image = models.ImageField(upload_to='images/degree_images/')
    cnic_image = models.ImageField(upload_to='images/cnic_images/')
    cnic_back = models.ImageField(upload_to='images/cnic_images/' , default=None, blank=True, null=True)
    cnic_number = models.CharField(max_length=15, default='' , null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)



class StudentProfile(Profile):
    subject = models.CharField(max_length=500, default='')
    institute = models.CharField(max_length=1000, default='')
    teaching_method = models.CharField(max_length=1000, default='')
    study_timing = models.CharField(max_length=1000,  default='')

    PREFERRED_TEACHER_CHOICES = [
        ('Male' , 'Male'),
        ('Female' , 'Female'),
    ]

    prefered_teacher = models.CharField(choices=PREFERRED_TEACHER_CHOICES, max_length=10 , default='Male' , blank=True, null=True)

    def __str__(self):
        return self.name

class TeacherProfile(Profile):
    # This is Profile Model for Teacher Role 
    # qualification 
    home_tution = models.BooleanField(default=False, null=True, blank=True)
    online_tutoring = models.BooleanField(default=False , null=True, blank=True)

    per_hour =models.CharField(max_length=6 , default='', blank=True, null=True)

    time_start = models.CharField(max_length=50 , default='')
    time_end = models.CharField(max_length=50 , default='')


    def __str__(self) :
        return self.name


class UserQualification(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_qualifications')
    
    degree = models.CharField(max_length=500, default='')
    subject = models.CharField(max_length=500, default='')
    passing_year = models.CharField(max_length=500, default='')
    institute = models.CharField(max_length=500, default='')


    def __str__(self) :
        return str(self.id)

class UserExperience(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_expriences')
    
    position = models.CharField(max_length=500, default='')
    from_date = models.CharField(max_length=500, default='')
    to_date = models.CharField(max_length=500, default='')
    institute = models.CharField(max_length=500, default='')
    exprience_years = models.CharField(max_length=500, default='')


    def __str__(self) :
        return str(self.id)

class UserReferences(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_references')
    
    name = models.CharField(max_length=500, default='')
    mobile_number = models.CharField(max_length=500, default='')
    email = models.CharField(max_length=500, default='')
    relation = models.CharField(max_length=500, default='')


    def __str__(self) :
        return str(self.id)

class UserMedia(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_medias')
    
    video = models.FileField(upload_to='tutor_videos/')

    def __str__(self) :
        return str(self.id)