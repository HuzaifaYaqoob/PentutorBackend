
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .models import Country, City, StudentQuery

from .serializers import CountrySerializer, CitySerializer
# Create your views here.



@api_view(['POST'])
@permission_classes([AllowAny])
def create_student_query(request):
    full_name = request.data.get('full_name', 'NA')
    email = request.data.get('email', 'NA')
    mobile_number = request.data.get('mobile_number', 'NA')
    city = request.data.get('city', 'NA')
    area = request.data.get('area', 'NA')

    StudentQuery.objects.create(
        full_name = full_name,
        email = email,
        mobile_number = mobile_number,
        city = city,
        area = area
    )

    return Response({
        'status' : True,
        'response' : {
            'message' : 'Created Successfully'
        }},
        status = status.HTTP_201_CREATED
    )

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
