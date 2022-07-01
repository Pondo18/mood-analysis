import os

import cv2


import tempfile

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from pages.usecases import AnalyseRecordedVideo


def index(request):
    return render(request, 'pages/index.html')


def analyse_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
    return render(request, 'pages/index.html')


@csrf_exempt
def analyse_recorded_video(request):
    if request.method == 'POST':
        blob_video = request.FILES['blob_video']
        analyse_recorded_video_use = AnalyseRecordedVideo(blob_video)
        analyse_recorded_video_use.execute()
    return render(request, 'pages/index.html')
