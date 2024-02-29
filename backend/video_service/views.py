from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from video_service.models import VideoFile
from video_service.serializers import VideoFileSerializer
from video_service.tasks import process_video
#import subprocess


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        video_file = request.data.get('video_file')
        video_file_instance = VideoFile.objects.create(
            video_file=video_file,
            filename=video_file.name)
        #serializer = VideoFileSerializer(video_file_instance)
        return Response({'id': str(video_file_instance.id)},
                        status=status.HTTP_200_OK)


class FileDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            video_file = VideoFile.objects.get(id=id)
            serializer = VideoFileSerializer(video_file)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VideoFile.DoesNotExist:
            return Response({'error': 'File not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id, *args, **kwargs):
        try:
            width = request.data.get('width')
            height = request.data.get('height')
            if (width is None or height is None or
                    width % 2 != 0 or height % 2 != 0
                    or width <= 20 or height <= 20):
                return Response({'error': 'Некорректная ширина или высота'},
                                status=status.HTTP_400_BAD_REQUEST)

            process_video.apply_async((id, width, height))

            return Response({'success': True}, status=status.HTTP_200_OK)
        except VideoFile.DoesNotExist:
            return Response({'error': 'File not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, *args, **kwargs):
        try:
            video_file = VideoFile.objects.get(id=id)
            video_file.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except VideoFile.DoesNotExist:
            return Response({'error': 'File not found'},
                            status=status.HTTP_404_NOT_FOUND)
