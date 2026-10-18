from django import forms
from .models import Department
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Fieldset,Submit

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name','users']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'dep_create'
        self.helper.layout = Layout(Fieldset("title","users"))
        self.helper.add_input(Submit('submit','Create'))


User = get_user_model()
class ManagerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ['username','password']
        labels = {"username":"Nazwa użytkownika", "password":"Hasło"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method='post'
        self.helper.form_action=''
        self.helper.layout = Layout(Fieldset("Dane użytkownika",'username','password'))
        self.helper.add_input(Submit('submit','Create'))

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.is_superuser=True
        user.is_staff=False
        if commit:
            user.save()
        return user