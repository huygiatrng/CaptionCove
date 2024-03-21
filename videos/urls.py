from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('delete/<uuid:video_id>/', delete_video, name='delete_video'),

]
