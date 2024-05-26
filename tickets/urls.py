from django.urls import path
from .views import *

urlpatterns = [
    path('', TicketAPIView.as_view()),
    path('<int:id>', TicketAPIViewById.as_view()),
    path('comment/', CommentAPIView.as_view()),
    path('comment/<int:id>', CommentAPIViewById.as_view())
]