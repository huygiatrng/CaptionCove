from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Video
import uuid
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
import os
from moviepy.editor import VideoFileClip
from django.conf import settings
import shutil


@login_required
@require_http_methods(['POST'])
def upload_video(request):
    if 'video' not in request.FILES:
        return JsonResponse({'error': 'No video file provided.'}, status=400)

    video_file = request.FILES['video']
    user = request.user
    unique_id = uuid.uuid4()  # Generate a unique ID for the video

    # Temporary save video file to calculate its duration
    temp_video_path = default_storage.save("temp_" + str(unique_id), video_file)
    temp_video_file = default_storage.path(temp_video_path)

    try:
        # Load the video file and calculate duration
        clip = VideoFileClip(temp_video_file)
        duration = int(clip.duration)  # Duration in seconds
    finally:
        # Ensure the video clip is closed before deleting the file
        clip.close()  # Make sure to close the clip to release the file
        # Ensure the temporary file gets deleted
        default_storage.delete(temp_video_path)

    # Create a new Video record and save it
    video = Video(user=user, name=video_file.name, unique_id=unique_id, duration=duration)
    video.file_path = video_file  # This will trigger the `upload_to` function
    video.save()

    return JsonResponse({'message': 'Video uploaded successfully', 'video_id': video.id, 'duration': duration})


@login_required
@require_http_methods(['DELETE'])
def delete_video(request, video_id):
    # Retrieve the video with the given ID and ensure it belongs to the current user
    video = get_object_or_404(Video, unique_id=video_id, user=request.user)

    # First, delete all related transcriptions and their files
    transcriptions = video.transcriptions.all()
    for transcription in transcriptions:
        transcription_dir = os.path.join(settings.MEDIA_ROOT, transcription.transcript_directory)
        # Check if the directory exists and delete it
        if os.path.exists(transcription_dir):
            shutil.rmtree(transcription_dir)
        # Delete the transcription record
        transcription.delete()

    # Now, delete the video files and directory
    if default_storage.exists(video.file_directory):
        # Delete all files in the directory
        for file in default_storage.listdir(video.file_directory)[1]:
            default_storage.delete(os.path.join(video.file_directory, file))
        # Delete the directory
        default_storage.delete(video.file_directory)

    # Finally, delete the video record itself from the database
    video.delete()

    return JsonResponse({'message': 'Video and all related transcriptions deleted successfully'})
