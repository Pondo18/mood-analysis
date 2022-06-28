from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def analyse_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
    return render(request, 'pages/index.html')


def analyse_recorded_video(request):
    if request.method == 'POST':
        recorded_video = request.POST['recorded_video']
    return render(request, 'pages/index.html')
