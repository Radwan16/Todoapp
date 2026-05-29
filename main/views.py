from django.shortcuts import render, redirect
from .models import Quest, Department , Project, Tag
from rest_framework import viewsets
from .serializer import QuestSerializer, UserSerializer, DepartmentSerializer ,ProjectSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import logout 
from django.contrib import messages
from datetime import date
from Tickets.models import Ticket
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions,status
from .mypermission import IsSuperUser
from django.utils.dateparse import parse_date
from django.http import HttpResponse
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def update(self, request ,*args, **kwargs):
        user = self.get_object()
        user.is_superuser = request.data['is_superuser']
        serializer = UserSerializer('auth.User', many=True)
        return Response(serializer.data)

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
            departament = Department.objects.get(users=request.user),
            tag = request.data['tag']

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
    
# class ProjectViewsSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    # serializer_class = ProjectSerializer

    # def create(self, request, *args, **kwargs):
    #     project = Project.objects.create(
    #         projectName = request.data['projectName'],
    #         managers = request.data["managers"]
    #     )
    #     serializer = ProjectSerializer(project,many=False)
    #     return Response(serializer.data)

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
    dep = request.user.departments.get() 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_superuser = bool(request.POST.get('is_superuser')) =='on'

        new_user = User.objects.create(
            username = username,
            is_superuser = is_superuser
        )
        new_user.set_password(password)
        new_user.save()
        try:
            dep.users.add(new_user)
        except:
            pass
    return render(request, "createnewuser.html")

@api_view(['GET','POST'])
@permission_classes([IsSuperUser])
def userupdate(request):
    current_user = request.user
    
    dep = current_user.departments.get() 
    
    if request.method == 'POST':
        users = dep.users.all()
        for user in users:
            is_super = f'is_superuser_{user.id}' in request.POST
            
            if user.is_superuser != is_super:
                user.is_superuser = is_super
                user.save()
        return redirect('userupdate')
        
    users = dep.users.all()
    return render(request, 'userupdate.html', {'users': users})


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

def createProject(request):
    managers=Department.objects.prefetch_related("users").all()
    if request.method == 'POST':
        projectName = request.POST.get('projectName')
        managers = request.POST.getlist('managers')
        new=Project.objects.create(projectName = projectName)
        if managers:
            new.managers.set(managers.id())
        return redirect('createProject')
    
    return render(request, 'createProjects.html',{"managers":managers})

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def home(request):
    dep = request.user.departments.get()
    users = dep.users.filter(is_superuser=False)
    departament_name = Department.objects.prefetch_related("users").get(users=request.user)
    return render(request, 'home.html', {'departament_name':departament_name, "users":users})

@api_view(['GET','POST'])
@permission_classes([IsSuperUser])
def questdetails(request, tag):
    dep = request.user.departments.get()
    if request.method == "GET":
        dead_line = request.GET.get('dead_line')
    filter_date = parse_date(str(dead_line)) if dead_line else date.today()
    quests = Quest.objects.filter(tag = tag, dead_line = filter_date, departament = dep)
    CheckDep = Quest.objects.filter(tag = tag, departament = dep)
    if not CheckDep.exists():
        return HttpResponse("<b><center>Ups. Wrong department or no quests found! <a href='/home/'>Return</a></center></b>")
    return render(request, "detailquest.html",{"quests":quests})