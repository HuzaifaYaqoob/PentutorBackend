from django.contrib import admin

# Register your models here.
from .models import Order, Invoice, OrderItems


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    search_fields = ['order_id']
    inlines=  [OrderItemsInline, InvoiceInline]
    list_display = [
        'order_id',
        'user',
        'status',
        'order_at',
    ]