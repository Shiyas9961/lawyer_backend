from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StatusModel

class StatusAPIView (APIView) :

    def get(self, request) :

        all_status = StatusModel.objects.all()
        all_status_list = []

        for status in all_status:
            status_obj = {
                "id" : status.id,
                "status_name" : status.status_name,
            }

            all_status_list.append(status_obj)
        
        return Response(all_status_list)
    
    def post(self, request) :

        new_status = StatusModel(status_name = request.data['status_name'])
        new_status.save()

        new_status_obj = {
            "id" : new_status.id,
            "status_name" : new_status.status_name
        }

        return Response(new_status_obj)

class StatusAPIViewById (APIView) :

    def get(self, request, id) :

        status_obj = StatusModel.objects.get(id = id)

        status_obj = {
            "id" : status_obj.id,
            "status_name" : status_obj.status_name
        }

        return Response(status_obj)
    
    def put(self, request, id):

        status_obj = StatusModel.objects.filter(id = id)
        status_obj.update(status_name = request.data['status_name'])
        updated_status = StatusModel.objects.get(id = id)

        status_obj = {
            "id" : updated_status.id,
            "status_name" : updated_status.status_name
        }

        return Response(status_obj)
    
    def delete (self, request, id) :

        status_obj = StatusModel.objects.get(id = id)
        name = status_obj.status_name
        status_obj.delete()

        return Response({
            "message" : f"Status {name} deleted successfully"
        })