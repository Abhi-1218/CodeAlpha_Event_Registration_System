from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'


class Registration(models.Model):
    STATUS_REGISTERED = 'registered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_REGISTERED, 'Registered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_REGISTERED)
    registered_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('participant', 'event')
        ordering = ['-registered_at']

    def __str__(self):
        return f'Registration for {self.participant.email} to {self.event.name}'
