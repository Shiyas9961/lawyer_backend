from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProjectModel
# Create your views here.
from .serializers import ProjectSerializer

class ProjectAPIView (APIView) :

    def get(self, request) :

        all_projects = ProjectModel.objects.all()
        all_project_list = []

        for project in all_projects:
            project_obj = {
                "id" : project.id,
                "project_name" : project.project_name,
                "tenand_id" : project.tenand_id
            }
            all_project_list.append(project_obj)
        
        return Response(all_project_list)
    
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

        project_obj = {
            "id" : project.id,
            "project_name" : project.project_name,
            "tenand_id" : project.tenand_id
        }

        return Response(project_obj)
    
    def put(self, request, id) :

        project = ProjectModel.objects.filter(id = id)
        project.update(project_name = request.data['project_name'], tenand_id = request.data['tenand_id'])

        project = ProjectModel.objects.get(id = id)
        project_obj = {
            "id" : project.id,
            "project_name" : project.project_name,
            "tenand_id" : project.tenand_id
        }

        return Response(project_obj)
    
    def delete(self, request, id) :

        project = ProjectModel.objects.get(id = id)
        name = project.project_name
        project.delete()

        return Response({
            "message" : f"Project {name} deleted successfully"
        })