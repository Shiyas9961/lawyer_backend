from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TicketModel, CommentModel
from .serializers import TicketSerializer, CommentSerializer
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
class CommentAPIView (APIView) :

    def get(self, request) :

        comments = CommentModel.objects.all()
        comments_ser = CommentSerializer(comments, many=True)

        return Response(comments_ser.data)
    
    def post(self, request) :

        data = request.data
        new_comment = CommentSerializer(data=data)

        if new_comment.is_valid() :
            new_comment.save()

            return Response(new_comment.data)
        else :
            return Response(new_comment.errors)
        
class CommentAPIViewById (APIView) :

    def get(self, request, id) :

        comment = CommentModel.objects.get(id = id)
        comment_ser = CommentSerializer(comment)

        return Response(comment_ser.data)
    
    def put(self, request, id) :

        data = request.data
        comment = CommentModel.objects.get(id = id)
        comment_ser = CommentSerializer(comment, data=data, partial = True)

        if comment_ser.is_valid() :
            comment_ser.save()

            return Response(comment_ser.data)
        else :
            return Response(comment_ser.errors)
        
    def delete(self, request, id) :

        comment = CommentModel.objects.get(id = id)
        ticket = comment.ticket.title
        comment.delete()

        return Response({
            "message" : f"Comment for {ticket} deleted"
        })