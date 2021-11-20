from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def LoginAPI(request):
    return JsonResponse({'hello' :'Working'})

def RegisterAPI(request):
    return JsonResponse({
        'Register' :'Register'
    })