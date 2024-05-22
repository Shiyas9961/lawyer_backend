from django.shortcuts import render
from .models import TenantModel
from rest_framework.views import APIView
from rest_framework.response import Response

class TenantAPIView (APIView) :

    def get(self, request) :

        all_tenants = TenantModel.objects.all()
        all_tenants_list = []

        for tenant in all_tenants:

            tenant_obj = {
                "id" : tenant.id,
                "tenant_name" : tenant.tenant_name,
                "phone_no" : tenant.phone_no,
                "email" : tenant.email,
            }

            all_tenants_list.append(tenant_obj)

        return Response(all_tenants_list)
    
    def post(self, request) :

        new_tenant = TenantModel(tenant_name = request.data['tenant_name'],phone_no = request.data['phone_no'], email = request.data['email'])
        new_tenant.save()
        tenant_obj = {
                "id" : new_tenant.id,
                "tenant_name" : new_tenant.tenant_name,
                "email" : new_tenant.email,
                "phone_no" : new_tenant.phone_no
            }
        
        return Response(tenant_obj)
    
class TenantAPIViewById (APIView) :
    def get (self, request, id) :
        tenant = TenantModel.objects.get(id = id)

        tenant_obj = {
            "id" : tenant.id,
            "tenant_name" : tenant.tenant_name,
            "email" : tenant.email,
            "phone_no" : tenant.phone_no
        }

        return Response(tenant_obj)
    
    def put(self, request, id) :

        tenant = TenantModel.objects.filter(id = id)
        tenant.update(tenant_name = request.data['tenant_name'],email = request.data['email'], phone_no = request.data['phone_no'])

        tenant = TenantModel.objects.get(id = id)
        tenant_obj = {
            "id" : tenant.id,
            "tenant_name" : tenant.tenant_name,
            "email" : tenant.email,
            "phone_no" : tenant.phone_no
        }

        return Response(tenant_obj)
    
    def delete(self, request, id) :

        tenant = TenantModel.objects.get(id = id)
        email = tenant.email
        tenant.delete()

        return Response({
            "message" : f"Tenant {email} deleted successfully"
        })