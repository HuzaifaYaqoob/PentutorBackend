from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from uuid import uuid4
from Course.models import Course

class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Cancelled', 'Cancelled'),
        ('Paid', 'Paid'),
    )
    order_id = models.CharField(max_length=999, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending', choices=ORDER_STATUS)
    order_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            total_orders = Order.objects.all().count()
            self.order_id = f'PTOR-{str(uuid4()).split("-")[0]}-{total_orders}'.upper()

        super(Order, self).save(*args, **kwargs)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=999, unique=True, editable=False)
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    invoice_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_id
    
    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.order.order_id
        super(Invoice, self).save(*args, **kwargs)