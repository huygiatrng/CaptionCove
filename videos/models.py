import os
from django.db import models
from django.contrib.auth.models import User
import uuid

def user_directory_path(instance, filename):
    # Extracts the name without the extension
    name, extension = os.path.splitext(filename)

    # Format: user_<username>/<video_name>_<video_uuid>/<filename>
    base_path = 'user_{0}/{1}_{2}'.format(instance.user.username, name, instance.unique_id)
    full_path = '{0}/{1}'.format(base_path, filename)

    # Set the file_directory on the instance
    instance.file_directory = os.path.dirname(full_path)

    return full_path

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=255)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    file_path = models.FileField(upload_to=user_directory_path)
    file_directory = models.CharField(max_length=255, editable=False, null=True)

    STATUS_CHOICES = (
        ('DO_NOTHING', 'Do Nothing'),
        ('TRANSCRIBING', 'Transcribing'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DO_NOTHING')
    duration = models.IntegerField(help_text="Duration in seconds")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
