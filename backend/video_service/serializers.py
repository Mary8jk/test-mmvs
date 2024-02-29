from video_service.models import VideoFile
from rest_framework import serializers


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ('id', 'filename', 'width', 'height',
                  'processing', 'processingSuccess')
