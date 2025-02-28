from django.db import models


class UploadedFile(models.Model):
    file = models.FileField()

    class Meta:
        verbose_name = "Uploaded File"
        verbose_name_plural = "Uploaded Files"
