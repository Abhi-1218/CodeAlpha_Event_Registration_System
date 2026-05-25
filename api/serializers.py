from rest_framework import serializers

from .models import Event, Participant, Registration


class EventSerializer(serializers.ModelSerializer):
    registration_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'location',
            'start_date',
            'end_date',
            'capacity',
            'registration_count',
        ]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']


class RegistrationDetailSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = [
            'id',
            'participant',
            'event',
            'status',
            'registered_at',
            'cancelled_at',
        ]


class RegistrationCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=120)
    last_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=30, allow_blank=True, required=False)
    event_id = serializers.IntegerField()

    def validate_event_id(self, value):
        try:
            event = Event.objects.get(pk=value)
        except Event.DoesNotExist:
            raise serializers.ValidationError('Event not found')
        return value

    def create(self, validated_data):
        event = Event.objects.get(pk=validated_data['event_id'])
        participant, created = Participant.objects.get_or_create(
            email=validated_data['email'].strip().lower(),
            defaults={
                'first_name': validated_data['first_name'].strip(),
                'last_name': validated_data['last_name'].strip(),
                'phone': validated_data.get('phone', '').strip(),
            },
        )

        if not created:
            participant.first_name = validated_data['first_name'].strip()
            participant.last_name = validated_data['last_name'].strip()
            participant.phone = validated_data.get('phone', '').strip()
            participant.save()

        active_count = event.registrations.filter(status=Registration.STATUS_REGISTERED).count()
        if event.capacity and active_count >= event.capacity:
            raise serializers.ValidationError('Event capacity has been reached')

        registration, reg_created = Registration.objects.get_or_create(
            participant=participant,
            event=event,
            defaults={'status': Registration.STATUS_REGISTERED},
        )

        if not reg_created and registration.status == Registration.STATUS_CANCELLED:
            registration.status = Registration.STATUS_REGISTERED
            registration.cancelled_at = None
            registration.save()
            return registration

        if not reg_created:
            raise serializers.ValidationError('User already registered for this event')

        return registration
