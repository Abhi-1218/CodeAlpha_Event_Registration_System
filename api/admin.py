from django.contrib import admin

from .models import Event, Participant, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'start_date', 'end_date', 'capacity')
    search_fields = ('name', 'location')
    list_filter = ('location',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'event', 'status', 'registered_at', 'cancelled_at')
    list_filter = ('status', 'event')
    search_fields = ('participant__email', 'event__name')
