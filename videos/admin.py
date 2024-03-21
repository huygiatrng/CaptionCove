from django.contrib import admin
from .models import Video
import os
from django.core.files.storage import default_storage


class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'unique_id', 'status', 'duration', 'created_at', 'updated_at')  # Added 'duration'
    list_filter = ('user', 'created_at', 'status')  # Consider adding 'status' if it's useful for your filtering needs
    search_fields = ('name', 'user__username', 'unique_id')
    actions = ['delete_with_files']

    def get_ordering(self, request):
        return ['created_at']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not obj:  # This means this is the "add" form, not the "edit" form.
            # Optionally remove fields not needed during creation
            fields = [f for f in fields if
                      f not in ('name', 'duration')]  # Assuming 'name' and 'duration' are automatically determined
        return fields

    def delete_with_files(self, request, queryset):
        for video in queryset:
            # Delete associated files from storage
            if default_storage.exists(video.file_directory):
                # Delete all files in the directory
                for file in default_storage.listdir(video.file_directory)[1]:
                    default_storage.delete(os.path.join(video.file_directory, file))
                # Then delete the directory itself
                default_storage.delete(video.file_directory)
            video.delete()
        self.message_user(request, "Selected videos and their files were successfully deleted.")

    delete_with_files.short_description = "Delete selected videos and their files"

    def save_model(self, request, obj, form, change):
        if not change:  # If adding a new Video
            # Since 'name' and 'duration' are determined automatically, no need to set them here
            pass
        super().save_model(request, obj, form, change)


admin.site.register(Video, VideoAdmin)
