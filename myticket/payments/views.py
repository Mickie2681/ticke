from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Ticket
from .serializers import TicketSerializer
from events.models import Event
from .mpesa import stk_push, get_access_token
from .tasks import send_ticket_email
import logging

logger = logging.getLogger(__name__)

class PaymentTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Test endpoint to check if M-Pesa integration is working"""
        try:
            # Test access token
            access_token = get_access_token()
            if access_token:
                return Response({
                    "status": "success",
                    "message": "M-Pesa integration is working",
                    "access_token": access_token[:20] + "..." if access_token else None
                })
            else:
                return Response({
                    "status": "error",
                    "message": "Failed to get M-Pesa access token"
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Payment test error: {str(e)}")
            return Response({
                "status": "error",
                "message": f"Payment service error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TicketPurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_id = request.data.get('event_id')
        phone_number = request.data.get('phone_number')  # M-Pesa phone
        
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not phone_number.startswith('254'):
            return Response({"error": "Phone number must start with 254"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            event = Event.objects.get(id=event_id)
            if event.available_tickets <= 0:
                return Response({"error": "No tickets available for this event"}, status=status.HTTP_400_BAD_REQUEST)

            # Initiate STK Push
            amount = int(event.ticket_price)
            account_reference = f"TICKET-{event.id}-{request.user.id}"
            transaction_desc = f"Payment for {event.name}"
            
            stk_response = stk_push(phone_number, amount, account_reference, transaction_desc)

            if 'errorCode' in stk_response:
                error_msg = stk_response.get('errorMessage', 'M-Pesa payment initiation failed')
                logger.error(f"M-Pesa STK Push failed: {stk_response}")
                return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if we got a valid response
            if 'CheckoutRequestID' not in stk_response:
                logger.error(f"Invalid M-Pesa response: {stk_response}")
                return Response({"error": "Invalid response from payment service"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Create pending ticket
            checkout_id = stk_response.get('CheckoutRequestID')
            ticket = Ticket.objects.create(
                user=request.user, 
                event=event, 
                checkout_id=checkout_id,
                payment_status='pending'
            )
            
            # Reserve the ticket by reducing available tickets
            event.available_tickets -= 1
            event.save()

            return Response({
                "message": "Payment initiated successfully. Check your phone for M-Pesa STK Push.",
                "checkout_id": checkout_id, 
                "ticket_id": ticket.id,
                "amount": amount
            }, status=status.HTTP_200_OK)
            
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in ticket purchase: {str(e)}")
            # Provide more specific error messages
            if "connection" in str(e).lower():
                return Response({"error": "Unable to connect to payment service. Please try again."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            elif "timeout" in str(e).lower():
                return Response({"error": "Payment service timeout. Please try again."}, status=status.HTTP_504_GATEWAY_TIMEOUT)
            else:
                return Response({"error": f"Payment processing error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MpesaCallbackView(APIView):
    permission_classes = []  # Public for M-Pesa callbacks

    def post(self, request):
        try:
            data = request.data.get('Body', {}).get('stkCallback', {})
            checkout_id = data.get('CheckoutRequestID')
            result_code = data.get('ResultCode')
            result_desc = data.get('ResultDesc', '')

            logger.info(f"M-Pesa callback received: {data}")

            if result_code == 0:  # Success
                # Find and update the ticket
                ticket = Ticket.objects.filter(checkout_id=checkout_id).first()
                if ticket:
                    ticket.payment_status = 'completed'
                    ticket.save()
                    
                    # Send confirmation email
                    try:
                        send_ticket_email.delay(ticket.id, ticket.user.email)
                    except Exception as e:
                        logger.error(f"Error sending ticket email: {str(e)}")
                    
                    logger.info(f"Payment completed for ticket {ticket.id}")
                else:
                    logger.error(f"Ticket not found for checkout_id: {checkout_id}")
            else:
                # Payment failed
                ticket = Ticket.objects.filter(checkout_id=checkout_id).first()
                if ticket:
                    ticket.payment_status = 'failed'
                    ticket.save()
                    
                    # Refund the ticket
                    event = ticket.event
                    event.available_tickets += 1
                    event.save()
                    
                    logger.error(f"Payment failed for ticket {ticket.id}: {result_desc}")
            
            return Response({"status": "OK"})
            
        except Exception as e:
            logger.error(f"Error processing M-Pesa callback: {str(e)}")
            return Response({"status": "ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TicketValidationView(APIView):
    permission_classes = [IsAuthenticated]  # Or admin only

    def post(self, request):
        unique_code = request.data.get('unique_code')
        try:
            ticket = Ticket.objects.get(unique_code=unique_code)
            if ticket.payment_status != 'completed':
                return Response({"error": "Ticket payment not completed"}, status=status.HTTP_400_BAD_REQUEST)
            if ticket.is_validated:
                return Response({"error": "Ticket already validated"}, status=status.HTTP_400_BAD_REQUEST)
            
            ticket.is_validated = True
            ticket.save()
            return Response({"message": "Ticket validated successfully"})
        except Ticket.DoesNotExist:
            return Response({"error": "Invalid ticket code"}, status=status.HTTP_404_NOT_FOUND)

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)