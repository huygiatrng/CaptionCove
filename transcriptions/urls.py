from django.urls import path
from . import views   # Adjust the import path if necessary

urlpatterns = [
    path('', views.home, name='home'),
    path('transcribe/', views.process_video, name='process_video'),
    path('transcribe_video/', views.transcribe_video, name='transcribe_video'),
    path('delete_transcription/<uuid:unique_id>/<str:model_type>/', views.delete_transcription, name='delete_transcription'),
    # ... other url patterns
]