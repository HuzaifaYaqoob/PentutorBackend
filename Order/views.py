from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

from Order.models import Order, OrderItems
from Course.models import Course, CartItem

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_course(request):
    items = CartItem.objects.filter(user=request.user)
    # Order.objects.create(
    #     user=request.user, 
    #     course=course,
    # )
    order = Order.objects.create(
        user=request.user, 
    )
    for item in items:
        OrderItems.objects.create(
            order=order,
            course=item.course
        )
        item.delete()

    return Response(
        {
            'status' : True,
            'message' : 'Order Placed Successfully',
            'id' : order.order_id
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkout_course(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, user=request.user)
    except:
        return Response(
            {
                'status' : False,
                'message' : 'Order Not Found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    data = {}
    
    return Response(
        {
            'data' : data,
        },
        status=status.HTTP_200_OK
    )