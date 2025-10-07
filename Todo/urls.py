from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main.views import UserViewSet, DepartmentViewSet,logout_view
from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views
from main.views import home
from main.models import Quest
from django.views.generic.dates import ArchiveIndexView
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'department',DepartmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('quest/',include('main.urls')),
    path('admin/', admin.site.urls),
    path('api-token/', views.obtain_auth_token),
    path('login/', auth_views.LoginView.as_view(),name="login"),
    path('logout/', logout_view, name="logout"),
    path('home/', home, name="home"),

]