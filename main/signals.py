from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()
@receiver(post_save, sender=User)
def create_admin_deparment(sender, instance=None, created=False, **kwargs):
    if created and instance.is_staff:
        try:
            Department.objects.get(name="admin").users.add(instance)
        except Department.DoesNotExist:
            dep = Department.objects.create(name="admin")
            dep.users.add(instance)
            print("The Admin Department has been created")