from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import GenericAPIView
from pdfsummarizer.tasks import process_pdf
from pdfsummarizer.serializers import PDFSerializer
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["PDF App"])
class HelloWorldView(APIView):
    def get(self, request):
        logger.info("Hello from PDF Summarizer!")
        return Response({"message": "Hello from PDF Summarizer!"})

@extend_schema(tags=["PDF App"])
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        logger.info(f"Hello, {request.user.username}!")
        return Response({"message": f"Hello, {request.user.username}!"})

@extend_schema(tags=["PDF App"])
class UploadPDF(GenericAPIView):
    serializer_class = PDFSerializer
    parser_classes = [MultiPartParser]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("PDF saved successfully")
            process_pdf.delay(serializer.instance.pdf_file.path)
            logger.info("PDF processing initiated...")
            return Response({"message": "PDF saved successfully"}, status=201)
        logger.error("something went wrong, pdf not saved")
        return Response({"message": "something went wrong, pdf not saved"}, status=400)
