from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProjectModel
# Create your views here.

class ProjectAPIView (APIView) :

    def get(self, request) :

        all_projects = ProjectModel.objects.all()
        all_project_list = []

        for project in all_projects:
            project_obj = {
                "id" : project.id,
                "project_name" : project.project_name
            }
            all_project_list.append(project_obj)
        
        return Response(all_project_list)
    
    def post(self, request) :

        new_project = ProjectModel(project_name = request.data['project_name'])
        new_project.save()
        project_obj = {
                "id" : new_project.id,
                "project_name" : new_project.project_name
            }
        
        return Response(project_obj)

    
class ProjectAPIViewById (APIView) :
    def get (self, request, id) :
        project = ProjectModel.objects.get(id = id)

        project_obj = {
            "id" : project.id,
            "project_name" : project.project_name
        }

        return Response(project_obj)
    
    def put(self, request, id) :

        project = ProjectModel.objects.filter(id = id)
        project.update(project_name = request.data['project_name'])

        project = ProjectModel.objects.get(id = id)
        project_obj = {
            "id" : project.id,
            "project_name" : project.project_name
        }

        return Response(project_obj)
    
    def delete(self, request, id) :

        project = ProjectModel.objects.get(id = id)
        name = project.project_name
        project.delete()

        return Response({
            "message" : f"Project {name} deleted successfully"
        })