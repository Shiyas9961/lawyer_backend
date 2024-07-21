from django.shortcuts import render
from .models import TenantModel
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TenantSerializer
from rest_framework.permissions import IsAuthenticated
from main_app.permissions import IsUserSuperAdmin
from main_app.authentication import CognitoAuthentication
from rest_framework import status

class TenantAPIView (APIView) :
    
    permission_classes = [IsAuthenticated, IsUserSuperAdmin]
    authentication_classes = [CognitoAuthentication]
    
    def get(self, request) :

        all_tenants = TenantModel.objects.all()
        all_tenants_ser = TenantSerializer(all_tenants, many=True)
        
        return Response(all_tenants_ser.data)
    
    def post(self, request) :

        data = request.data
        new_tenant = TenantSerializer(data=data)

        if new_tenant.is_valid() :
            new_tenant.save()

            return Response({
                "message" : "New tenant created"
            }, status=status.HTTP_201_CREATED)
        else :
            return Response(new_tenant.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TenantAPIViewById (APIView) :

    def get (self, request, id) :
        tenant = TenantModel.objects.get(id = id)
        tenant_ser = TenantSerializer(tenant)

        return Response(tenant_ser.data)
    
    def put(self, request, id) :

        data = request.data
        tenant = TenantModel.objects.get(id = id)
        tenant_ser = TenantSerializer(tenant, data=data, partial=True)

        if tenant_ser.is_valid() :
            tenant_ser.save()

            return Response({
                "message" : "Tenant updated successfully"
            }, status=status.HTTP_202_ACCEPTED)
        else :
            return Response(tenant_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id) :

        tenant = TenantModel.objects.get(id = id)
        email = tenant.email
        tenant.delete()

        return Response({
            "message" : f"Tenant {email} deleted successfully"
        })