from django.urls import path
from .views import GeneratePDF

urlpatterns = [
    path('pdf/', GeneratePDF.as_view()),
]