from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.username

class Movie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    producer = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    duration = models.IntegerField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Studio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    seat_capacity = models.IntegerField()

    def __str__(self):
        return self.name

class StudioManager(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

class Seat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)

    class Meta:
        unique_together = ('studio', 'seat_number')

    def __str__(self):
        return f'{self.studio.name} - {self.seat_number}'


class Showtime(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        unique_together = ('movie', 'studio', 'start_time')

    def __str__(self):
        return f'{self.movie.name} at {self.studio.name}'

class Reservation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.showtime}'

class ReservedSeat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seat', 'showtime', 'reservation')
