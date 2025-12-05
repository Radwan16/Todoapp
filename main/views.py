from django.shortcuts import render, redirect
from .models import Quest, Department
from rest_framework import viewsets
from .serializer import QuestSerializer, UserSerializer, DepartmentSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import logout 
from django.contrib import messages
from datetime import date
from Tickets.models import Ticket
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .mypermission import IsSuperUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class= DepartmentSerializer

    def update(self, request, *args, **kwargs):
        department = self.get_object()
        department.name = request.data['department']
        department.users = request.data['users']
        serializer = DepartmentSerializer('department',many=False)
        return Response(serializer.data)

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer

    def create(self, request, *args, **kwargs):
        quest = Quest.objects.create(
            title = request.data['title'],
            description = request.data['description'],
            dead_line = request.data['dead_line'],
            assigned_to = User.objects.get(id=request.POST['assigned_to']),
            departament = Department.objects.get(users=request.user)

        )
        serializer = QuestSerializer(quest,many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        quest = self.get_object()
        quest.title= request.data['title']
        quest.description= request.data['description']
        quest.dead_line= request.data['dead_line']
        quest.made=request.data['made', False]
        quest.assigned_to= (request.data['assigned_to'])
        quest.departament= request.data['departament']
        quest.comment= request.data['comment']
        quest.save()
        serializer = QuestSerializer(quest,many=False)
        return Response(serializer.data)

def logout_view(request):
    logout(request)
    return redirect('login')

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def listuserquest(request):   
    if request.method == 'POST':
        quest_ids = request.POST.getlist('quests')
        ticket_ids = request.POST.getlist('tickets')

        for quest_id in quest_ids:
            if quest_id:
                comment = request.POST.get(f'comment_{quest_id}','')
                Quest.objects.select_related("departament").filter(id__in=quest_ids).update(made=True, comment=comment)

        for ticket_id in ticket_ids:
            if ticket_id:
                Ticket.objects.select_related("departament").filter(id__in=ticket_ids).update(made=True)

        return redirect('listuserquest')
    
    tickets = Ticket.objects.select_related("assigned_to").filter(made=False, assigned_to=request.user)
    quests = Quest.objects.select_related("assigned_to").filter(made=False, assigned_to=request.user) 
    return render(request, 'tasklist.html', {'quests':quests,'tickets':tickets,'today':date.today()})

@api_view(['GET','POST'])
@permission_classes([IsSuperUser])
def createuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_superuser = bool(request.POST.get('is_superuser'))


        new_user = User(username=username)
        new_user.set_password(password)
        new_user.is_superuser = is_superuser
        new_user.save()
        # dep = Department.objects.prefetch_related("users").filter(users=request.user).first()
        # dep.users.add(user)
        
    return render(request,'createnewuser.html')

@api_view(['GET','POST'])
@permission_classes([IsSuperUser])
def createquest(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        dead_line = request.POST.get('dead_line')
        assigned_to_id = request.POST.get('assigned_to')
        u = Department.objects.prefetch_related("users").get(users=request.user)
        Quest.objects.create(
            title=title,
            description=description,
            dead_line=dead_line,
            assigned_to_id=assigned_to_id,
            departament=u 
        )
        return redirect('createquest')
    u = Department.objects.prefetch_related("users").get(users=request.user)
    usersid = u.users.all() if u else []
    return render(request, 'createquest.html', {'usersid': usersid})
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def not_completed(request):
    if request.method=='POST':
        quest_ids = request.POST.getlist('quests')
        for quest_id in quest_ids:
            comment = request.POST.get(f'comment_{quest_id}','')
            Quest.objects.select_related("assigned_to").filter(id__in=quest_ids).update(made=True, comment=comment)
        return redirect('not_completed')
    quests = Quest.objects.filter(made=False, departament=Department.objects.select_related().get(users=request.user), dead_line__lt = date.today(), assigned_to=request.user) 
    return render(request, 'not_completed.html', {'quests':quests})

@api_view(['GET','POST'])
@permission_classes([IsSuperUser])
def history(request):
    if request.method == 'POST':
        quests_ids = request.POST.getlist('quests')
        for quests_id in quests_ids:
            Quest.objects.filter(id__in=quests_ids).update(made=False)
    dep=Department.objects.prefetch_related("users").get(users=request.user)
    quests=Quest.objects.select_related("assigned_to").filter(departament=dep)
    tickets=Ticket.objects.select_related("assigned_to").filter(departament=dep)
    return render(request, 'history.html',{'quests':quests, 'tickets':tickets})
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def home(request):
    departament_name = Department.objects.prefetch_related("users").get(users=request.user)
    return render(request, 'home.html', {'departament_name':departament_name})