from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Table {self.table_number} (Seats {self.capacity})'

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    special_request = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reservation_date', '-reservation_time']
    
    def __str__(self):
        return f'Reservation for {self.user.username} on {self.reservation_date} at {self.reservation_time}'
    
    def get_end_time(self):
        reservation_datetime = datetime.combine(
            self.reservation_date, 
            self.reservation_time
        )
        end_datetime = reservation_datetime + timedelta(hours=2)
        return end_datetime.time()
