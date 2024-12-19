from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', login_view , name='login'),
    path('H',HV.as_view(), name='H'),
]
