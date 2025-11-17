from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class Upload(models.Model):
  class UploadState(models.TextChoices):
    UPLOADED = "UP", "Uploaded"
    STARTED = "ST", "Processing started"
    # P1,P2,P3 for the stages of processing
    DONE = "DO", "Done"
    CANCEL = "CA", "Cancelled"
    DELETED = "DE", "Deleted"
        
  file = models.FileField(
    validators=[FileExtensionValidator(allowed_extensions=['csv'])],
    upload_to="data/ingest/"
  )

  state = models.CharField(max_length=2, choices=UploadState, default=UploadState.UPLOADED)  
  def __str__(self):
    return f"Upload(file={self.file},state={self.state})"
