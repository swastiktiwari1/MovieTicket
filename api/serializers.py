from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields= '__all__'

class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields= '__all__'

class TheatreSerializerNoScreen(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields= ['name','city']

class TheatreScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreScreen
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields= '__all__'

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields= '__all__'

class ShowSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSeat
        fields= '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields= '__all__'



