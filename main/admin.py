from django.contrib import admin
from .models import Quest, Department, Tag #Project
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Department)
# admin.site.register(Project)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("user",)}
class QuestAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','dead_line','made','assigned_to','departament','comment','tag')
    prepopulated_fields = {"tag":("assigned_to",)}

admin.site.register(Quest,QuestAdmin)