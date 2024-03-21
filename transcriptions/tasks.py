from celery import shared_task
from .services import WhisperTranscriber
from django.conf import settings
from django.contrib.auth.models import User
from videos.models import Video
from .models import Transcription
import os
from django.db import transaction

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def transcribe_video_task(unique_id, model_type, user_username):
    try:
        print("TESTING")
        video = Video.objects.get(unique_id=unique_id)
        logger.info("Video object fetched.")

        logger.info("Fetching user object from DB.")
        user = User.objects.get(username=user_username)
        logger.info("User object fetched.")

        video.status = 'TRANSCRIBING'
        video.save()

        video_file_path = os.path.join(settings.MEDIA_ROOT, video.file_path.name)
        transcriber = WhisperTranscriber(user_username, model_size=model_type,
                                         output_dir=os.path.dirname(video_file_path))
        transcript_file_paths = transcriber.transcribe(video_file_path)

        # Check if the transcription already exists
        transcription_exists = Transcription.objects.filter(video=video, model_type=model_type).exists()

        # Assuming the transcription was successful, determine the directory path
        if transcript_file_paths and not transcription_exists:
            # Use the directory of the first transcript file as the reference path
            transcript_directory = os.path.dirname(transcript_file_paths[0])

            # Create only one Transcription object with the path to the transcript files directory
            Transcription.objects.create(
                video=video,
                user=user,
                model_type=model_type,
                transcript_directory=transcript_directory
            )
            logger.info("New Transcription object created.")
        elif transcription_exists:
            logger.info("Transcription already exists. Skipping object creation.")

        video.status = 'DO_NOTHING'
        video.save()
        logger.info("Task completed successfully.")
    except Exception as e:
        video = Video.objects.get(unique_id=unique_id)
        video.status = 'DO_NOTHING'
        video.save()
        print(f"Error:{e}")