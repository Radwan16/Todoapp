from django.db.models.signals import post_save
from django.dispatch import receiver
from Tickets.models import Ticket
from webpush import send_user_notification
from django.contrib.auth.models import User
@receiver(post_save, sender=Ticket)
def ticket_get_recipient(sender, instance, created, **kwargs):
        if not created :
                
                payload = {"head": "Welcome!", "body": "Hello World"}
                send_user_notification(user=User.objects.get(username="Tytus"), payload=payload, ttl=120)
                # print("Warunki spełnione")
                # payload={
                #     "head":"Your ticket has a recipient !",
                #     "body": f"Ticket assigned to {instance.assigned_to}"
                # }
                # send_user_notification(user=instance.who, payload=payload)
                # print("Powiadomienie wysłane")
