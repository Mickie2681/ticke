from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name', read_only=True)
    event_date = serializers.DateTimeField(source='event.date', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'unique_code', 'checkout_id', 'payment_status', 
            'is_validated', 'purchase_date', 'event_name', 'event_date', 
            'event_location', 'user_name'
        ]
        read_only_fields = ['id', 'unique_code', 'checkout_id', 'purchase_date']