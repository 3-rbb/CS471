from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),                      # /books/
    path('index2/<int:val1>/', views.index2),   # /books/index2/5/
]