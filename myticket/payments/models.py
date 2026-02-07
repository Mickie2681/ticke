from django.db import models
from django.conf import settings
from events.models import Event
import uuid

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    checkout_id = models.CharField(max_length=100, blank=True, null=True)  # M-Pesa checkout ID
    payment_status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    is_validated = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.event.name} - {self.user.username}"
    
    class Meta:
        ordering = ['-purchase_date']