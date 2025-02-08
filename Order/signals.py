
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Order, Invoice


@receiver(post_save, sender=Order)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        Invoice.objects.create(order=instance)