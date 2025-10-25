from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializer import TicketSerializer
from .models import Ticket
from rest_framework.response import Response
from main.models import Department

class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        ticket = Ticket.objects.create(
            title = request.data['title'],
            description = request.data['description'],
            who = request.data['who'],
            departament = request.data['departament'],
        )

        serializer = TicketSerializer(ticket, many=False)
        return Response(serializer.data)
    
def ticketsdb(request):
    if request.method == 'POST':
        ticket_ids = request.POST.getlist('tickets')
        for ticket_id in ticket_ids:
            Ticket.objects.filter(id__in=ticket_ids).update( assigned_to = request.user.id)
        return redirect('ticketsdb')
    dep = Department.objects.prefetch_related("users").get(users=request.user)
    userids = dep.users.all() if dep else[] 
    tickets = Ticket.objects.filter(departament = Department.objects.select_related().get(users=request.user))
    return render(request,'ticketsdb.html',{'tickets':tickets, 'userids':userids})

def createtickets(request):
    departament = Department.objects.all()
    if request.method =='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        departament_id = Department.objects.get(id=request.POST.get('departament_id'))
        Ticket.objects.create(
            title = title,
            description = description,
            who = request.user,
            departament = departament_id
        )
        
        return redirect('createtickets')
    return render(request, 'createticket.html', {'dep':departament})

