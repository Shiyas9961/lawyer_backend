from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProjectModel
# Create your views here.
from .serializers import ProjectSerializer

class ProjectAPIView (APIView) :

    def get(self, request) :

        all_projects = ProjectModel.objects.all()
        all_projects_ser = ProjectSerializer(all_projects, many=True)
        
        return Response(all_projects_ser.data)
    
    def post(self, request) :

        new_project = ProjectSerializer(data = request.data)

        if new_project.is_valid() :
            new_project.save()

            return Response(new_project.data)
        else :
            return Response(new_project.errors)
    
class ProjectAPIViewById (APIView) :

    def get (self, request, id) :
        project = ProjectModel.objects.get(id = id)
        project_ser = ProjectSerializer(project)
        return Response(project_ser.data)
    
    def put(self, request, id) :

        data = request.data
        project = ProjectModel.objects.get(id = id)
        project_ser = ProjectSerializer(project, data=data, partial=True)

        if project_ser.is_valid() :
            project_ser.save()

            return Response(project_ser.data)
        else :
            return Response(project_ser.errors)
    
    def delete(self, request, id) :

        project = ProjectModel.objects.get(id = id)
        name = project.project_name
        project.delete()

        return Response({
            "message" : f"Project {name} deleted successfully"
        })