from django.urls import path
from .views import HelloWorldView, ProtectedView

urlpatterns = [
    path('hello/', HelloWorldView.as_view()),
    path('protected/', ProtectedView.as_view()),
]
