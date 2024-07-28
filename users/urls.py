from django.urls import path
from .views import ListUsersByTenant, UserAPIView, UserAPIViewById

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('user/<str:id>/', UserAPIViewById.as_view()),
    path('t-users/', ListUsersByTenant.as_view()),
]
