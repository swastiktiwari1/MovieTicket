from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import SwaggerDict 
# Create your views here.

class MovieAPIView(APIView):
    def get(self,request):
        """
        returns a list of all movies
        """
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie,many = True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=MovieSerializer)
    def post(self, request):
        """
        creates a new movie
        """
        serializer = MovieSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TheatreAPIView(APIView):
    def get(self, request):
        """
        returns a list of all theatres
        """
        movie = Theatre.objects.all()
        serializer = TheatreSerializer(movie,many = True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=TheatreSerializerNoScreen)
    def post(self, request):
        """
        creates a new theatre
        """
        serializer = TheatreSerializerNoScreen(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TheatreScreenAPIView(APIView):
    def get(self,request):
        """
        returns a list of all TheatreScreens
        """
        theatre_screen = TheatreScreen.objects.all()
        serializer = TheatreScreenSerializer(theatre_screen,many = True)
        return Response(serializer.data)
    def get_theatre_object(self,pk):
        try:
            return  Theatre.objects.get(theatre_id=pk)
        except Theatre.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(request_body=TheatreScreenSerializer)
    def post(self, request):
        """
        creates a new TheatreScreen
        """
        serializer = TheatreScreenSerializer(data= request.data)
        
        if serializer.is_valid():
            theatre = self.get_theatre_object(request.data['theatre'])
            theatre.total_screens+=1;
            theatre.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    def get(self,request):
        """
        returns a list of all Users
        """
        user = User.objects.all()
        serializer = UserSerializer(user,many = True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        """
        creates a new User
        """
        serializer = UserSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CityAPIView(APIView):
    def get(self,request):
        """
        returns a list of all Citys
        """
        city = City.objects.all()
        serializer = CitySerializer(city,many = True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=CitySerializer)
    def post(self, request):
        """
        creates a new City
        """
        serializer = CitySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowAPIView(APIView):
    def get(self,request):
        """
        returns a list of all Shows
        """
        show = Show.objects.all()
        serializer = ShowSerializer(show,many = True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=ShowSerializer)
    def post(self, request):
        """
        creates a new Show
        """
        serializer = ShowSerializer(data= request.data)
        
        if serializer.is_valid():
            screen_id = request.data['theatre_screen']
            screen = TheatreScreen.objects.get(screen_id=screen_id)
            for seats in range(screen.total_seats):
                seat = ShowSeat(seat_num=seats+1,show=Show.objects.get(show_id=serializer.data['show_id']))
                seat.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingAPIView(APIView):
    def get(self,request):
        """
        returns a list of all Bookings
        """
        booking = Booking.objects.all()
        serializer = BookingSerializer(booking,many = True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=BookingSerializer)
    def post(self, request):
        """
        creates a new Booking
        """
        serializer = BookingSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            seat = ShowSeat.objects.get(shoow_seat_id=request.data['show_seat'])
            seat.status = True
            seat.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CityMovieAPIView(APIView):
    def get_movie(self,pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,pk):
        """
        get all the cities in which the movie is avilable
        """
        movie = self.get_movie(pk)
        shows = Show.objects.filter(movie=movie)
        screens =set()
        for show in shows:
            screens.add(show.theatre_screen)
        theatres = set()
        for screen in screens:
            theatres.add(screen.theatre)
        cities = set()
        for theatre in theatres:
            cities.add(theatre.city.city_id)
        return Response(list(cities))
    
class TheatreFromCityAndMovieAPIView(APIView):
    def get_movie(self,pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    def get_city(self,pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,city_key,movie_key):
        """
        Get theatre in the city with movie given as argument 
        """
        movie = self.get_movie(movie_key)
        city = self.get_city(city_key)
        theatres_in_city=Theatre.objects.filter(city=city)
        theatre_screen = TheatreScreen.objects.filter(theatre__in= theatres_in_city)
        shows = Show.objects.filter(theatre_screen__in=theatre_screen)
        theatre = set()
        for show in shows:
            theatre.add(show.theatre_screen.theatre)
        return Response(TheatreSerializer(theatre,many=True).data)

class TheatreToShowAPIView(APIView):    
    def get(self,request,pk):
        """
        Get Shows available in the given theatre
        """
        theatre = Theatre.objects.filter(theatre_id=pk)
        theatre_screens = TheatreScreen.objects.filter(theatre__in = theatre)
        shows = Show.objects.filter(theatre_screen__in = theatre_screens)
        return Response(ShowSerializer(shows,many=True).data)

class ShowToSeatAPIView(APIView):
    def get(self,request,pk):
        """
        Get Booked and Non booked seats for current show 
        """
        show = Show.objects.filter(show_id = pk)
        seats = ShowSeat.objects.filter(show__in = show)
        booked = ShowSeatSerializer(seats.filter(status=True),many=True).data
        non_booked = ShowSeatSerializer(seats.filter(status=False),many=True).data
        d=dict()
        d["booked"]=booked
        d["non booked"]=non_booked
        return Response(d)
        