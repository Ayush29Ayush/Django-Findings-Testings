from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from dummyapp.models import DummyModel
from dummyapp.serializers import DummyModelSerializer
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Dummy App"])
class DummyListCreateView(generics.ListCreateAPIView):
    queryset = DummyModel.objects.all()
    serializer_class = DummyModelSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'creations' # This applies the 'creations' scope rate limit (20/hour) to this view
    
    # Cache GET requests for 2 minutes, create a separate cache per user using Authorization
    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        logger.info(f"Created DummyModel with id={instance.id}, sum={instance.sum}")
        return Response({"message": "Record calculated and saved successfully.","sum": instance.sum}, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Dummy App"])
class DummyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DummyModel.objects.all()
    serializer_class = DummyModelSerializer
    permission_classes = [IsAuthenticated]
    #! If we don't set a custom ScopedRateThrottle, this view will use the default 'user' throttle rate (1000/day) from settings.py
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'details'

    # Cache GET detail requests for 15 minutes, create a separate cache per user using Authorization
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
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
