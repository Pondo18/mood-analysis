from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse_uploaded_file', views.analyse_uploaded_file, name='analyse-uploaded-file'),
    path('analyse_recorded_video', views.analyse_recorded_video, name='analyse-recorded-video')
]
