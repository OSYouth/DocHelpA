from django.urls import path
from . import views

urlpatterns = [
    path('upload_success', views.upload_success),
    path('upload_error', views.upload_error),
    path('download_grade_analysis/<str:name>', views.download_grade_analysis),
]