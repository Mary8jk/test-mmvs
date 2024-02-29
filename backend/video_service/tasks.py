from celery import shared_task
import subprocess
from .models import VideoFile
from django.http import JsonResponse


@shared_task
def process_video(id, width, height):
    try:
        video_file = VideoFile.objects.get(id=id)
        video_file.processing = True
        video_file.processingSuccess = False
        video_file.save()

        command = ['ffmpeg', '-i', video_file.video_file.path, 
                   '-vf', 'scale={}:{}'.format(width, height),
                   '-c:a', 'copy', 'output.mp4']
        process = subprocess.Popen(command)
        process.communicate()

        video_file.width = width
        video_file.height = height
        video_file.processing = False
        video_file.processingSuccess = True
        video_file.save()
    except VideoFile.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        video_file.processing = False
        video_file.processingSuccess = False
        video_file.save()
        return JsonResponse({'error': str(e)}, status=500)
