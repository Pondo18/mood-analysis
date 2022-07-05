from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from pages.usecases import AnalyseVideo, AnalyseImage


def index(request):
    return render(request, 'pages/index.html')


def analyse_uploaded_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.content_type == 'image/jpeg':
            analyse_image_use = AnalyseImage(file)
            frame, emotion = analyse_image_use.execute()
        else:
            analyse_video_use = AnalyseVideo(file)
            frame, emotion = analyse_video_use.execute()
    return render(request, 'pages/index.html', {'frames': frame, 'emotion': emotion})


@csrf_exempt
def analyse_recorded_video(request):
    if request.method == 'POST':
        blob_video = request.FILES['blob_video']
        analyse_recorded_video_use = AnalyseVideo(blob_video)
        frames, final_emotion = analyse_recorded_video_use.execute()
    return render(request, 'pages/index.html', {'frames': frames, 'emotion': final_emotion})
