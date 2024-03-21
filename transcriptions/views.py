from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from videos.models import Video
from users.models import User
from django.conf import settings
from .models import Transcription
from .services import WhisperTranscriber  # Ensure this import path is correct
import os
from .tasks import transcribe_video_task
from django.shortcuts import get_object_or_404
import shutil


@csrf_exempt  # Disable CSRF for simplicity, consider CSRF protection for production
@require_http_methods(["POST"])  # Only accept POST requests
def process_video(request):
    username = request.user.username
    if 'video' not in request.FILES:
        return JsonResponse({'error': 'No video file provided.'}, status=400)

    video_file = request.FILES['video']
    transcriber = WhisperTranscriber(username)  # Pass the username
    transcript_file_path = transcriber.transcribe(video_file.temporary_file_path())

    if os.path.exists(transcript_file_path):
        with open(transcript_file_path, 'r') as file:
            transcript_content = file.read()
        return JsonResponse({'transcript': transcript_content})
    else:
        return JsonResponse({'error': 'Transcription failed.'}, status=500)


@login_required
@require_http_methods(["POST"])
def transcribe_video(request):
    user = request.user
    unique_id = request.POST.get('unique_id')
    model_type = request.POST.get('model_type', 'base')

    try:
        video = Video.objects.get(unique_id=unique_id, user=user)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)

    # Check if the video status allows for transcription
    if video.status != 'DO_NOTHING':
        return JsonResponse({'error': 'Transcription cannot be initiated at this moment. Please try again later.'},
                            status=400)

    # Trigger the Celery task
    transcribe_video_task.delay(unique_id, model_type, user.username)

    return JsonResponse({'message': 'Transcription has been initiated. Please check back later for the status.'})


@login_required
@require_http_methods(["DELETE"])
def delete_transcription(request, unique_id, model_type):
    # Ensure the user is authenticated and has access to the video
    user = request.user

    # Try to get the video with the given unique_id that belongs to the user
    video = get_object_or_404(Video, unique_id=unique_id, user=user)

    # Try to get the transcription associated with the video and model_type
    try:
        transcription = Transcription.objects.get(video=video, model_type=model_type)
    except Transcription.DoesNotExist:
        return JsonResponse({'error': 'Transcription not found'}, status=404)

    # Construct the path to the transcription directory
    transcription_dir = os.path.join(settings.MEDIA_ROOT, transcription.transcript_directory)

    # Check if the directory exists and delete it
    if os.path.exists(transcription_dir):
        shutil.rmtree(transcription_dir)
        # Optionally, you can also delete the Transcription record from the database
        transcription.delete()
        return JsonResponse({'message': 'Transcription deleted successfully'})
    else:
        return JsonResponse({'error': 'Transcription directory does not exist'}, status=404)


def home(request):
    return HttpResponse("Welcome to the Transcribe API!")
