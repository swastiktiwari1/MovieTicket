from django.urls import path
from .views import *
urlpatterns = [
     path('movie/', MovieAPIView.as_view()),
     path('theatre/', TheatreAPIView.as_view()),
     path('user/',UserAPIView.as_view()),
     path('city/',CityAPIView.as_view()),
     path('theatrescreen/', TheatreScreenAPIView.as_view()),
     path('user/',UserAPIView.as_view()),
     path('show/',ShowAPIView.as_view()),
     path('booking/',BookingAPIView.as_view()),
     path('movie/<int:pk>/city/',CityMovieAPIView.as_view()),
     path('movie/<int:movie_key>/city/<int:city_key>/theatre',TheatreFromCityAndMovieAPIView.as_view()),
     path('theatre/<int:pk>/shows/',TheatreToShowAPIView.as_view()),
     path('show/<int:pk>/showseats/',ShowToSeatAPIView.as_view())

]