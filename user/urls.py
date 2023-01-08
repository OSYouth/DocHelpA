from django.urls import path
from . import views

urlpatterns = [
    path('upload_user_list', views.batch_create_user),
    path('upload_error', views.upload_error)
]