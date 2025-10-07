from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils.text import slugify
from django.urls import reverse

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Department(models.Model):
    name = models.CharField(max_length=25)
    users = models.ManyToManyField(User, related_name="departments")
    def __str__(self):
        return f'{self.name}'
    
class Tag(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.user} user slug name: {self.slug}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        return super().save(*args, **kwargs)

class Quest(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=255)
    dead_line = models.DateField(null=True, blank=True)
    update = models.DateTimeField(auto_now_add=True)
    made = models.BooleanField(default=False)
    assigned_to = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    departament = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, related_name='quests')
    comment= models.CharField(max_length=100 ,blank=True, null=True)
    def __str__(self):
        return f"{self.title}, {self.dead_line}, {self.made}"