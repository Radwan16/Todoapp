from rest_framework import serializers
from .models import Ticket
from django.contrib.auth.models import User
from main.models import Department
class TicketSerializer(serializers.ModelSerializer):
    who=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    departament=serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Ticket
        fields = ['title','description','made','assigned_to','who','departament','comment']
