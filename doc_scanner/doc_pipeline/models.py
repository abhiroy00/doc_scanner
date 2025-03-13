from django.db import models

# Create your models here.
from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ocr_text = models.TextField(blank=True, null=True)
    extracted_info = models.TextField(blank=True, null=True)