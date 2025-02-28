from django.db import models


class UploadedFile(models.Model):
    file = models.FileField()

    def __str__(self):
        return self.file

    class Meta:
        verbose_name = "Uploaded File"
        verbose_name_plural = "Uploaded Files"
