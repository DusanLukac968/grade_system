from django import forms
from .models import User, Teacher, Parent, Student, Classes, Subjects
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet
from django.contrib.auth import login, logout, authenticate, get_user_model
def class_choices():
    choices = []
    
    for class_name in Classes.objects.all():
        choices.append((class_name.id,class_name.class_name))
        
    return choices

def subject_name_choices():
    choices = []
    for  subject in Subjects.objects.all():
        choices.append((subject.id ,subject.subject_name))
    return choices

def user_name_opions():
    choices = []
    for user in User.objects.all():
        choices.append((user.user_id, user.get_full_name))
    return choices

class UserRegistrationForm(UserCreationForm):

    limited_choice = [User.USER_LEVEL_CHOICES[0]]
    user_level = forms.ChoiceField(choices=limited_choice)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["name", "surname", "tel", "email",]

class TeacherRegistrationForm(UserCreationForm):
    
    limited_choice = [User.USER_LEVEL_CHOICES[2]]
    user_level = forms.ChoiceField(choices=limited_choice)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["name", "surname", "date_of_birth", "tel", "email", "user_level",]

class StudentRegistrationForm(UserCreationForm):
    
    limited_choice = [User.USER_LEVEL_CHOICES[3]]
    user_level = forms.ChoiceField(choices=limited_choice)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["name", "surname", "date_of_birth", "tel", "email", "user_level",]

class LoginForm(forms.Form):
    """
    regular login form asking only email and password for multiple purposses
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ["email", 'password']

class SubjectAdd(forms.ModelForm):

    class Meta:
        model = Subjects
        fields = ["subject_name", "subject_short"]


class SubjectRemove(forms.ModelForm):

    subject_name = forms.ChoiceField(choices=subject_name_choices)

    class Meta:
        model = Subjects
        fields = ["subject_name"]

class ClassesAdd(forms.ModelForm):

    class Meta:
        model = Classes
        fields = ["class_name"]

class ClassesRemove(forms.ModelForm):

    class_name = forms.ChoiceField(choices=class_choices)
    class Meta:
        model = Classes
        fields = ["class_name"]

class UserUpdateForm(forms.ModelForm):

    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField()
    date_of_birth = forms.DateField()
    tel = forms.CharField()
    
    class Meta:
        model = User
        fields = ["email", "name", "surname", "date_of_birth", "tel"]

class TeacherAdvanceRegister(forms.ModelForm):
    user = forms.ChoiceField(choices=user_name_opions)
    subjects = forms.MultipleChoiceField(choices= subject_name_choices, widget= forms.CheckboxSelectMultiple, label='Taught Subjects')
    classes = forms.MultipleChoiceField(choices= class_choices, widget= forms.CheckboxSelectMultiple, label='Teaching in')

    class Meta:
        model = Teacher
        fields = ["user", "subjects", "classes"]

class StudentAdvanceRegister(forms.ModelForm):
    user = forms.ChoiceField(choices=user_name_opions)
    subjects = forms.MultipleChoiceField(choices= subject_name_choices, widget= forms.CheckboxSelectMultiple)
    classes = forms.MultipleChoiceField(choices= class_choices, widget= forms.CheckboxSelectMultiple)

    class Meta:
        model = Teacher
        fields = ["user", "subjects", "classes"]

    
"""subjects = forms.MultipleChoiceField(choices=subject_choices(), widget=forms.CheckboxSelectMultiple)
    classes = forms.MultipleChoiceField(choices=class_choices(), widget=forms.CheckboxSelectMultiple)"""