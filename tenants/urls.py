from django.urls import path
from .views import *

urlpatterns = [
    path('', TenantAPIView.as_view()),
    path('<int:id>', TenantAPIViewById.as_view())
]