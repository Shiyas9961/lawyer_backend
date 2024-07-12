from rest_framework import serializers
from .models import TicketModel, CommentModel

class TicketSerializer(serializers.ModelSerializer) :

    class Meta :
        model = TicketModel
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer) :

    class Meta :
        model =  CommentModel
        fields = "__all__"  