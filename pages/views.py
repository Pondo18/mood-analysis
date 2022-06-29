from django.shortcuts import render
from pages import emotion_detection

# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def analyse_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        result = emotion_detection.emotion_detection(image)
        print(result)
    return render(request, 'pages/index.html')


def analyse_recorded_video(request):
    if request.method == 'POST':
        recorded_video = request.POST['recorded_video']
    return render(request, 'pages/index.html')
