from django.db import models
import uuid


class VideoFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='video_files/')
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    processing = models.BooleanField(default=False)
    processingSuccess = models.BooleanField(null=True)

    def __str__(self):
        return self.filename
