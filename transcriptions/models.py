from django.db import models
from videos.models import Video
from django.contrib.auth.models import User


class Transcription(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='transcriptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_type = models.CharField(max_length=100)
    transcript_directory = models.CharField(max_length=255, help_text="Path to the transcription files directory",
                                            null=True)
    def __str__(self):
        return f"{self.video.name} - {self.model_type}"
