from django.urls import path
from . import views

urlpatterns = [
    path('download', views.download),
    path('download_test/<str:name>', views.download_test),
]