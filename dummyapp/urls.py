from django.urls import path
from .views import DummyListCreateView, DummyRetrieveUpdateDestroyView

urlpatterns = [
    path('model/', DummyListCreateView.as_view(), name='dummy-model-list-create'),
    path('model/<int:pk>/', DummyRetrieveUpdateDestroyView.as_view(), name='dummy-model-detail'),
]
