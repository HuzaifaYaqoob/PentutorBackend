
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Country, City

from .serializers import CountrySerializer, CitySerializer
# Create your views here.


class GetCountries(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_countries = Country.objects.all()
        serialized_obj = CountrySerializer(all_countries, many=True)

        return Response(
            {
                'status': 'OK',
                'message': 'Request Successful',
                'response': serialized_obj.data
            },
                status=status.HTTP_200_OK

        )


class GetCities(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            ctry = Country.objects.get(id = request.GET.get('country'))
        except Country.DoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Country Does Not Exist',
                },
                status= status.HTTP_404_NOT_FOUND
            )
        else:
            serialized_obj = CitySerializer(ctry.country_cities , many=True)
            print(ctry.country_cities )
            return Response(
                {
                    'status': 'OK',
                    'message': 'Request Successful',
                    'response': serialized_obj.data
                },
                status=status.HTTP_200_OK
            )
