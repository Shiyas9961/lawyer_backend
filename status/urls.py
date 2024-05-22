from django.urls import path
from .views import *

urlpatterns = [
    path('', StatusAPIView.as_view()),
    path('<int:id>', StatusAPIViewById.as_view())
]
