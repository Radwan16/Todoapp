from django.contrib import admin
from .models import Quest, Department, Tag
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
admin.site.register(Quest)
admin.site.register(Department)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("user",)}
