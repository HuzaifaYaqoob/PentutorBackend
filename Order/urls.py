

from django.urls import path, include

from . import views

urlpatterns = [
    path('checkout_course/' , views.checkout_course),
    path('get_order/<str:order_id>/' , views.checkout_course),
]
