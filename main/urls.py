from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main import views
router = routers.DefaultRouter()
router.register(r'', views.QuestViewSet)
urlpatterns=[
    path('Createuser/', views.createuser, name="createuser"),
    path('tasklist/', views.listuserquest, name="listuserquest"),
    path('createquest/',views.createquest, name="createquest"),
    path('history/',views.history, name="history"),
    path('not_completed/',views.not_completed,name="not_completed"),
    path('',include(router.urls)),
    
]
