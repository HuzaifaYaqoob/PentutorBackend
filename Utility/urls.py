

from django.urls import path

from . import views

urlpatterns = [
    path('get_all_countries/' , views.GetCountries.as_view() , name='Get_All_Countries' ),
    path('get_cities/' , views.GetCities.as_view() , name='GET_COUNTRY_CITIES' ),
]