from django.urls import path
from .views import *

urlpatterns = [
    path('', ProjectAPIView.as_view()),
    path('<int:id>', ProjectAPIViewById.as_view())
]