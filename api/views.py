from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Participant, Registration
from .serializers import (
    EventSerializer,
    RegistrationCreateSerializer,
    RegistrationDetailSerializer,
)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.annotate(
        registration_count=Count('registrations', filter=Q(registrations__status=Registration.STATUS_REGISTERED))
    )
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.annotate(
        registration_count=Count('registrations', filter=Q(registrations__status=Registration.STATUS_REGISTERED))
    )
    serializer_class = EventSerializer


class RegistrationCreateView(APIView):
    def post(self, request):
        serializer = RegistrationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()
        output = RegistrationDetailSerializer(registration)
        return Response(output.data, status=status.HTTP_201_CREATED)


class RegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationDetailSerializer

    def get_queryset(self):
        queryset = Registration.objects.select_related('participant', 'event')
        user_email = self.request.query_params.get('userEmail')
        event_id = self.request.query_params.get('eventId')

        if user_email:
            queryset = queryset.filter(participant__email__iexact=user_email.strip())
        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset.order_by('-registered_at')


class RegistrationCancelView(APIView):
    def delete(self, request, pk):
        try:
            registration = Registration.objects.get(pk=pk)
        except Registration.DoesNotExist:
            return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)

        if registration.status == Registration.STATUS_CANCELLED:
            return Response({'error': 'Registration already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        registration.status = Registration.STATUS_CANCELLED
        registration.cancelled_at = timezone.now()
        registration.save()
        return Response({'message': 'Registration cancelled successfully'})
