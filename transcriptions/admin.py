from django.contrib import admin
from django.core.files.storage import default_storage
from .models import Transcription
import shutil
from django.conf import settings
import os

class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'created_at', 'updated_at', 'model_type')
    search_fields = ('video__name', 'user__username', 'model_type')  # Assuming video has a 'name' field
    list_filter = ('created_at', 'updated_at', 'model_type', 'user')
    actions = ['delete_transcriptions_and_folders']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('video', 'user')

    def delete_transcriptions_and_folders(modeladmin, request, queryset):
        for transcription in queryset:
            transcription_dir = os.path.join(settings.MEDIA_ROOT, transcription.transcript_directory)
            if os.path.exists(transcription_dir):
                shutil.rmtree(transcription_dir)
            transcription.delete()
        modeladmin.message_user(request, "Selected transcriptions and their folders were successfully deleted.")
    delete_transcriptions_and_folders.short_description = "Delete selected transcriptions and their folders"

admin.site.register(Transcription, TranscriptionAdmin)
