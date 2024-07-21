from django.urls import path
from .views import *

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('<str:id>/', UserAPIViewById.as_view()),
    path('t-users/', ListUsersByTenant.as_view())
]
