from django.db import models

# Create your models here.



class HomePageAdmin(models.Model):
    hero_section_image = models.ImageField(upload_to='administration/home_page/' , null = True, blank=True)
    