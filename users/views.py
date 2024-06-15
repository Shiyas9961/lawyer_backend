import hmac
import hashlib
import base64
import boto3
from .models import UserModel
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserModelsSerializer, UserRegisterSerializer
from main_app.authentication import CognitoAuthentication
from main_app.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.conf  import settings
from rest_framework import status
# Create your views here.

def get_secret_hash(username, client_id, client_secret) :

    message = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

class UserAPIView(APIView) :

    permission_classes = [ IsAuthenticated, IsAdminUser ]
    authentication_classes = [ CognitoAuthentication, ]

    def get(self, request) :

        all_users = UserModel.objects.all()
        all_users_serial = UserModelsSerializer(all_users, many=True).data

        return Response(all_users_serial)

    def post(self, request) :

        data = request.data
        data['role'] = data.get('role', 'user')
        data['tenand_id'] = request.user.tenand_id
        serializer = UserRegisterSerializer(data=data)
        
        if serializer.is_valid() :

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            role = serializer.validated_data['role']
            phone_no = serializer.validated_data['phone_no']
            tenand_id = serializer.validated_data['tenand_id']

            client_id = settings.COGNITO_APP_CLIENT_ID
            client_secret = settings.COGNITO_APP_CLIENT_SECRET
            secret_hash = get_secret_hash(email, client_id, client_secret)

            client = boto3.client('cognito-idp', region_name = settings.COGNITO_REGION)

            try:
                response = client.sign_up(
                    ClientId = client_id,
                    SecretHash = secret_hash,
                    Username = email,
                    Password = password,
                    UserAttributes = [
                        { 'Name' : 'custom:role', 'Value' : role },
                        { 'Name' : 'email', 'Value' : email },
                        { 'Name' : 'name', 'Value' : username },
                        { 'Name' : 'custom:tenand_id', 'Value' : str(tenand_id) },
                        { 'Name' : 'phone_number', 'Value' : phone_no }
                    ]
                )
                
                if response and response['UserConfirmed'] :

                    user_sub = response['UserSub']  # User unique identifier
                    # user_confirmed = response['UserConfirmed']  Check if the user is confirmed
                    
                    user_details = {
                        'user_id': user_sub,
                        'username': username,
                        'email': email,
                        'phone_no' : phone_no,
                        'tenant' : tenand_id
                    }

                    new_user = UserModelsSerializer(data = user_details)

                    if new_user.is_valid() :
                        new_user.save()
                        return Response(new_user.data)
                    else :
                        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)

            except client.exceptions.UsernameExistsException as e :
                return Response({"error" : "username already exist"}, status=status.HTTP_400_BAD_REQUEST)
            except client.exceptions.InvalidPasswordException as e :
                return Response({"error" : "invalid password provided"}, status=status.HTTP_400_BAD_REQUEST)
            except client.exceptions.UserLambdaValidationException as e :
                return Response({"error" : "invalid password provided"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e :
                return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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