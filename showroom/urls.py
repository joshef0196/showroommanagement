from showroom import views
from django.urls import path

urlpatterns = [
    path('dashboard/', views.index),
    path('', views.login),
    path('logout/', views.logout),
]
