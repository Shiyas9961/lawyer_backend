from django.urls import path
from .views import *

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('<int:id>', UserAPIViewById.as_view())
]
