from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TicketModel
from .serializers import TicketSerializer
from users.models import UserModel
# Create your views here.

class TicketAPIView (APIView) :

    def get (self, request) :

        tickets = TicketModel.objects.all()
        all_tickets = TicketSerializer(tickets, many=True).data

        return Response(all_tickets)

    def post (self, request) :
        
        tenant = UserModel.objects.get(tenant= request.data['user']).tenant

        new_ticket = TicketModel(title = request.data['title'], description = request.data['description'], project_id = request.data['project'], status_id = request.data['status'], user_id = request.data['user'], tenant_id = tenant.id)

        new_ticket.save()

        ticket = TicketSerializer(new_ticket).data

        return Response(ticket)

class TicketAPIViewById (APIView) :

    def get (self, request, id) :

        ticket = TicketModel.objects.get(id = id)
        ticket_obj = TicketSerializer(ticket).data

        return Response(ticket_obj)

    def put (self, request, id) :
        
        ticket = TicketModel.objects.get(id = id)
        updated_ticket = TicketSerializer(ticket, data=request.data, partial = True)

        if updated_ticket.is_valid() :
            updated_ticket.save()

            return Response(updated_ticket.data)
        else :
            return Response(updated_ticket.errors)

    def delete (self, request, id) :
         
        ticket = TicketModel.objects.get(id = id)
        name = ticket.title
        ticket.delete()

        return Response({
            "message" : f"Ticket {name} deleted"
        })