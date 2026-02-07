from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_qr_code
import os

@shared_task
def send_ticket_email(ticket_id, email):
    from .models import Ticket
    ticket = Ticket.objects.get(id=ticket_id)
    qr_file = generate_qr_code(ticket.unique_code)
    ticket.qr_code.save(f"{ticket.unique_code}.png", qr_file)
    ticket.save()

    subject = f"Ticket for {ticket.event.name}"
    body = f"Dear {ticket.user.username},\n\nYour ticket is attached.\nUnique Code: {ticket.unique_code}"
    email_msg = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [email])
    email_msg.attach(f"{ticket.unique_code}.png", ticket.qr_code.read(), 'image/png')
    email_msg.send()