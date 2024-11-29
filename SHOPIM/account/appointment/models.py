# appointment/models.py
from django.db import models
from users.models import CustomUser

class Appointment(models.Model):
    BOOKING_CHOICES = [
        ('Grooming', 'Grooming'),
        ('Boarding', 'Boarding'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments',default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contact = models.CharField(max_length=11)
    date = models.DateField()
    time = models.TimeField()
    booking_type = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='Grooming')


    def __str__(self):
        return self.email
