from django.db import models

class PDFSaver(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')