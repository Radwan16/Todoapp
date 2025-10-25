from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Tickets import views
router = routers.DefaultRouter()
router.register(r'', views.TicketsViewSet)

urlpatterns = [
    path('ticketsdb/',views.ticketsdb, name="ticketsdb"),
    path('createtickets/', views.createtickets, name="createtickets"),
    path('',include(router.urls) )
]