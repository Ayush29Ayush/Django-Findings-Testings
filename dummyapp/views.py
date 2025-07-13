from rest_framework import generics
from .models import DummyModel
from .serializers import DummyModelSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Dummy App"])
class DummyListCreateView(generics.ListCreateAPIView):
    queryset = DummyModel.objects.all()
    serializer_class = DummyModelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        logger.info(f"Created DummyModel with id={instance.id}, sum={instance.sum}")
        return Response({
            "message": "Record calculated and saved successfully.",
            "sum": instance.sum
        }, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Dummy App"])
class DummyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DummyModel.objects.all()
    serializer_class = DummyModelSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(f"Retrieved DummyModel id={instance.id}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(f"Update requested for DummyModel id={instance.id} with data: {request.data}")
        response = super().update(request, *args, **kwargs)
        logger.info(f"Updated DummyModel id={instance.id} — new sum={response.data.get('sum')}")
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.warning(f"Deleting DummyModel id={instance.id}")
        return super().destroy(request, *args, **kwargs)
