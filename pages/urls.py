from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse_image', views.analyse_image, name='analyse-image'),
    path('analyse_recorded_video', views.analyse_recorded_video, name='analyse-recorded-video')
]
