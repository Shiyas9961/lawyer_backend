import boto3
from .models import UserModel
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserModelsSerializer, UserRegisterSerializer, UserLoginSerializer
from main_app.authentication import CognitoAuthentication
from main_app.permissions import IsAdminUser, IsUserUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf  import settings
from rest_framework import status
# Create your views here.


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
        data['tenand_id'] = request.user.tenant
        serializer = UserRegisterSerializer(data=data)
        
        if serializer.is_valid() :

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            role = serializer.validated_data['role']
            phone_no = serializer.validated_data['phone_no']
            tenand_id = serializer.validated_data['tenand_id']

            client_id = settings.COGNITO_APP_CLIENT_ID

            client = boto3.client('cognito-idp', region_name = settings.COGNITO_REGION)

            try:
                response = client.sign_up(
                    ClientId = client_id,
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

    permission_classes = [IsAuthenticated, IsUserUser]
    authentication_classes = [ CognitoAuthentication ]
    
    def get(self, request, id) :

        user = UserModel.objects.get(pk = id)
        user_serializer = UserModelsSerializer(user).data

        return Response(user_serializer, status=status.HTTP_200_OK)
    
    def put(self, request, id) :

        user_id = request.user.user_id
        role = request.user.role

        if (user_id == id) or (role in ["admin", "superadmin"]) :
            
            curr_user = UserModel.objects.get(pk = id)

            name = request.data.get('username')
            phone_no = request.data.get('phone_no')
            new_role = None

            if role in ["admin", "superadmin"] :
                new_role = request.data.get("role", new_role)

            if not name and not phone_no :
                return Response({
                    "message" : "Name or Phone number required"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            client = boto3.client('cognito-idp', region_name = settings.COGNITO_REGION)
            
            user_attributes = []

            if name :
                user_attributes.append({
                    'Name' : 'name', 'Value' : name
                })
            if phone_no :
                user_attributes.append({
                    'Name' : 'phone_number', 'Value' : phone_no
                })
            if new_role :
                user_attributes.append({
                    'Name' : 'custom:role', 'Value' : new_role
                })
            try:

                response = client.admin_update_user_attributes(
                    UserPoolId = settings.COGNITO_USER_POOL_ID,
                    Username = curr_user.email,
                    UserAttributes = user_attributes
                )

                if response and (response['ResponseMetadata']['HTTPStatusCode'] == 200) :
                    curr_user_ser = UserModelsSerializer(curr_user, data=request.data, partial=True)
                    if curr_user_ser.is_valid() :
                        curr_user_ser.save()
                        return Response({
                            "message" : "User details updated"
                            }, status=status.HTTP_200_OK)
                    else :
                        return Response(curr_user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
            except client.exceptions.UserNotFoundException:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e :
                return Response({
                    "message" : str(e)
                }, status=status.HTTP_400_BAD_REQUEST)    
        else :
            return Response({
                "message" : "You have no permission to edit the details of this user"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete (self, request, id) :

        if request.user.role in ["admin", "superadmin"] :
            
            user = UserModel.objects.get(pk = id)
            client = boto3.client('cognito-idp', region_name = settings.COGNITO_REGION)

            try:
                response = client.admin_delete_user(
                    UserPoolId = settings.COGNITO_USER_POOL_ID,
                    Username = user.email
                )

                if response and (response['ResponseMetadata']['HTTPStatusCode'] == 200) :
                    user.delete()
                    return Response({
                        "message" : f"User deleted successfully"
                    })
            except client.exceptions.UserNotFoundException:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e :
                return Response({
                    "message" : str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response({
                "message" : "You have no permission to delete the user"
            }, status=status.HTTP_401_UNAUTHORIZED)
            
class ListUsersByTenant(APIView) :

    permission_classes = [ IsAuthenticated, IsAdminUser ]
    authentication_classes = [ CognitoAuthentication ]

    def get(self, request) :
        tenant = request.user.tenant
        users_by_tenant = UserModel.objects.filter(tenant=tenant)
        serializer = UserModelsSerializer(users_by_tenant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    
# class UserLoginAPIView(APIView) :

#     permission_classes = [ AllowAny ]

#     def post(self, request) :

#         data = request.data
#         serializer = UserLoginSerializer(data=data)

#         if serializer.is_valid() :
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']

#             client = boto3.client('cognito-idp', region_name = settings.COGNITO_REGION)
#             try :
#                 response = client.initiate_auth(
#                         AuthFlow = 'USER_PASSWORD_AUTH',
#                         AuthParameters = {
#                             'USERNAME' : username,
#                             'PASSWORD' : password
#                         },
#                         ClientId = settings.COGNITO_APP_CLIENT_ID
#                     )
#                 return Response(response['AuthenticationResult'], status=status.HTTP_202_ACCEPTED)
#             except client.exceptions.NoAuthorizedException :
#                 return Response({
#                     "message" : "Invalid username or password"
#                 }, status=status.HTTP_400_BAD_REQUEST)
#             except Exception as e :
#                 return Response({
#                     "message" : str(e)
#                 }, status=status.HTTP_400_BAD_REQUEST)