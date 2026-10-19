from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main import views
router = routers.DefaultRouter()
router.register(r'', views.QuestViewSet)
app_name = 'main'
urlpatterns=[
    path('Createuser/', views.createuser, name="createuser"),
    path('tasklist/', views.listuserquest, name="listuserquest"),
    path('createquest/',views.createquest, name="createquest"),
    path('history/',views.history, name="history"),
    path('not_completed/',views.not_completed,name="not_completed"),
    path('<slug:tag>', views.questdetails, name="detailquest"),
    path('depcreate/', views.dep_create, name="depcreate"),
    path('managercreate/', views.manager_create, name="managercreate"),
    path('',include(router.urls))
    
]
