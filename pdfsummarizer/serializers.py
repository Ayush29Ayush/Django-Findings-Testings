from rest_framework import serializers
from pdfsummarizer.models import *

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFSaver
        fields = '__all__'