from django.db import models

class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="datasets/")
    summary = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"
