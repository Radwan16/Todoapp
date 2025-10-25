from django.db import models
from main.models import Department
class Ticket(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=255)
    made = models.BooleanField(default=False)
    assigned_to = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    who = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    departament = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, related_name='tickets')
    comment= models.CharField(max_length=100 ,blank=True, null=True)
    def __str__(self):
        return f"{self.title},{self.made}, {self.who},{self.assigned_to}"
