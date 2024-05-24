from django.shortcuts import render
from .models import UserModel
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserModelsSerializer
# Create your views here.

class UserAPIView(APIView) :

    def get(self, request) :

        all_users = UserModel.objects.all()
        all_users_serial = UserModelsSerializer(all_users, many=True).data

        return Response(all_users_serial)
    
    def post(self, request) :

        new_user = UserModelsSerializer(data = request.data)

        if new_user.is_valid() :
            new_user.save()
            return Response(new_user.data)
        else :
            return Response(new_user.errors)
        
class UserAPIViewById (APIView) :

    def get(self, request, id) :

        user = UserModel.objects.get(id = id)
        user_serializer = UserModelsSerializer(user).data

        return Response(user_serializer)
    
    def put(self, request, id) :

        user = UserModel.objects.get(id = id)
        user_serializer = UserModelsSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid() :
            user_serializer.save()

            return Response(user_serializer.data)
        else :
            return Response(user_serializer.errors)
        
    def delete (self, request, id) :

        user = UserModel.objects.get(id = id)
        name = user.username
        user.delete()

        return Response({
            "message" : f"User {name} deleted successfully"
        })