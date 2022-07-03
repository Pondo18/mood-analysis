from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from pages.usecases import AnalyseRecordedVideo, AnalyseImage


def index(request):
    return render(request, 'pages/index.html')


def analyse_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        analyse_image_use = AnalyseImage(image)
        frame = analyse_image_use.execute()
        if len(frame) == 0:
            return render(request, 'pages/index.html')
        else:
            return render(request, 'pages/index.html', {'frames': frame, 'emotion': frame[0].emotion})


@csrf_exempt
def analyse_recorded_video(request):
    if request.method == 'POST':
        blob_video = request.FILES['blob_video']
        analyse_recorded_video_use = AnalyseRecordedVideo(blob_video)
        frames, final_emotion = analyse_recorded_video_use.execute()
    return render(request, 'pages/index.html', {'frames': frames, 'emotion': final_emotion})
