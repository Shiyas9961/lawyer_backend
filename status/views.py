from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StatusModel
from .serializers import StatusSerializer

class StatusAPIView (APIView) :

    def get(self, request) :

        all_status = StatusModel.objects.all()
        all_status_ser = StatusSerializer(all_status, many=True)
        
        return Response(all_status_ser.data)
    
    def post(self, request) :

        data = request.data
        new_status = StatusSerializer(data=data)

        if new_status.is_valid():
            new_status.save()

            return Response(new_status.data)
        else :
            return Response(new_status.errors)

class StatusAPIViewById (APIView) :

    def get(self, request, id) :

        status_obj = StatusModel.objects.get(id = id)
        status_obj_ser = StatusSerializer(status_obj)

        return Response(status_obj_ser.data)
    
    def put(self, request, id):

        data = request.data
        status_obj = StatusModel.objects.get(id = id)
        status_obj_ser = StatusSerializer(status_obj, data=data, partial=True)

        if status_obj_ser.is_valid() :
            status_obj_ser.save()

            return Response(status_obj_ser.data)
        else :
            return Response(status_obj_ser.errors)
    
    def delete (self, request, id) :

        status_obj = StatusModel.objects.get(id = id)
        name = status_obj.status_name
        status_obj.delete()

        return Response({
            "message" : f"Status {name} deleted successfully"
        })