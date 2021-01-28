from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    duration = models.TimeField()
    language = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=1000)
    def __str__(self):
        return self.title

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Theatre(models.Model):
    theatre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    total_screens = models.IntegerField(default=0)
    city = models.ForeignKey(City, on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class TheatreScreen(models.Model):
    screen_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    total_seats = models.IntegerField()
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Show(models.Model):
    show_id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    theatre_screen = models.ForeignKey(TheatreScreen, on_delete= models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.PROTECT,blank=True,null=True)
    def __str__(self):
        return str(self.start_time)+" "+str(self.end_time)

class ShowSeat(models.Model):
    shoow_seat_id = models.AutoField(primary_key=True)
    seat_num = models.IntegerField()
    status = models.BooleanField(default=False)
    price = models.FloatField(default=300) 
    show = models.ForeignKey(Show,on_delete = models.CASCADE)
    def __str__(self):
        return self.shoow_seat_id



class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    show_seat = models.OneToOneField(ShowSeat,blank=False,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.booking_id