from django.urls import path
from .views import HelloWorldView, ProtectedView, UploadPDF

urlpatterns = [
    path('hello/', HelloWorldView.as_view()),
    path('protected/', ProtectedView.as_view()),
    path('uploadpdf/', UploadPDF.as_view()),
]
