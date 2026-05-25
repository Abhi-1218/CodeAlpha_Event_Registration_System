from django.urls import path

from .views import (
    EventDetailView,
    EventListView,
    RegistrationCancelView,
    RegistrationCreateView,
    RegistrationListView,
)

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('register/', RegistrationCreateView.as_view(), name='register'),
    path('registrations/', RegistrationListView.as_view(), name='registration-list'),
    path('registrations/<int:pk>/', RegistrationCancelView.as_view(), name='registration-cancel'),
]
