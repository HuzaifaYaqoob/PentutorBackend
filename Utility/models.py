from django.db import models

from django.utils.timezone import now
import uuid

# Create your models here.


class Country(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, unique=True , default=uuid.uuid4)
    
    name = models.CharField(max_length=1000, default='')
    code = models.CharField(max_length=50, default='' , blank=True, null=True)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.UUIDField(auto_created=True, unique=True, primary_key=True, default=uuid.uuid4)
    country = models.ForeignKey(Country, default=None, related_name='country_states', on_delete=models.CASCADE)

    name = models.CharField(max_length=1000, default='')
    code = models.CharField(max_length=50, default='', blank=True , null=True)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self) :
        return self.name

class City(models.Model):
    id = models.UUIDField(auto_created=True, unique=True, primary_key=True, default=uuid.uuid4)
    country = models.ForeignKey(Country, default=None, related_name='country_cities', on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=None, null=True, blank=True, related_name='state_cities', on_delete=models.CASCADE)

    name = models.CharField(max_length=1000, default='')
    code = models.CharField(max_length=50, default='', blank=True , null=True)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self) :
        return self.name