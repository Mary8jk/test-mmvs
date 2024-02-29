from django.urls import path
from video_service.views import FileUploadView, FileDetailView

urlpatterns = [
    path('file/', FileUploadView.as_view(), name='file-upload'),
    path('file/<uuid:id>/', FileDetailView.as_view(), name='file-detail'),
]
