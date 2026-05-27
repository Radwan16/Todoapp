from rest_framework import serializers
from .models import Quest , Department ,Project
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = User
        fields = ['url', 'username','password','is_superuser']
        extra_kwargs = {'password':{'required':True,'write_only':True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields=['name','users']

class QuestSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field = 'username', queryset=User.objects.all())
    class Meta:
        model = Quest
        fields = ['id','title', 'description','dead_line','made','assigned_to','departament','comment','tag']
        read_only_fields=('departament',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["projectName","managers"]