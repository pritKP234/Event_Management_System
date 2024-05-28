from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

User = get_user_model

class User(AbstractUser):
    social_id = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=11, choices=[('organizer', 'Organizer'), ('participant', 'Participant')])
    groups = models.ManyToManyField(
        Group,
        related_name='event_mgmnt_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='event_mgmnt_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    privacy = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')])
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='events')
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
