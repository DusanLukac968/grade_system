from django import forms
from .models import User, Teacher, Parent, Student, Classes, Subjects
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet
from django.contrib.auth import login, logout, authenticate, get_user_model

"""FUNCTIONS """
def class_choices():
    """
    simple function returns class name for choice fields
    """
    choices = []
    for class_name in Classes.objects.all():
        choices.append((class_name.id,class_name.class_name))
    return choices

def subject_name_choices():
    """
    simple function returns subject name for choice fields
    """
    choices = []
    for  subject in Subjects.objects.all():
        choices.append((subject.id ,subject.subject_name))
    return choices

def user_name_opions():
    """
    simple function returns user name for choice fields using user get_full_name function
    """
    choices = []
    for user in User.objects.all():
        choices.append((user.user_id, user.get_full_name))
    return choices

def teacher_name_opions():
    """
    simple function returns teacher name for choice fields
    takes all users with user_role teacher and uses user function get_full_name
    """
    choices = []
    for user in User.objects.all():
        if user.user_level == 2:
            choices.append((user.user_id, user.get_full_name))
    return choices

def student_name_opions():
    """
    simple function returns student name for choice fields
    takes all users with user_role student and uses user function get_full_name
    """
    choices = []
    for user in User.objects.all():
        if user.user_level == 3:
            choices.append((user.user_id, user.get_full_name))
    return choices

def parent_name_options():
    """
    simple function returns parents names for choice fields
    takes all users with user_role parent and uses user function get_full_name
    """
    choices= []
    for user in User.objects.all():
        if user.user_level == 4:
            choices.append((user.user_id, user.get_full_name))
    return choices

"""REGISTRATION FORMS"""
class UserRegistrationForm(UserCreationForm):
    """
    form for user registration with fixed user_role to 0 [admin]
    """
    choices = User.USER_LEVEL_CHOICES
    user_level = forms.ChoiceField(choices=choices)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["name", "surname", "date_of_birth", "tel", "email", "user_level",]


"""LOGIN FORM"""
class LoginForm(forms.Form):
    """
    regular login form asking only email and password for multiple purposses
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ["email", 'password']

"ADDITIONAL FORMS"
class SubjectAdd(forms.ModelForm):
    """
    form used for creation new subjects asking for subject name and its shortcut for further use in school schedule
    """
    class Meta:
        model = Subjects
        fields = ["subject_name", "subject_short"]


class ClassesAdd(forms.ModelForm):
    """
    form used for creating new classes, asking for class name
    """
    class Meta:
        model = Classes
        fields = ["class_name"]

"""UPDATE FORMS"""
class UserUpdateForm(forms.ModelForm):
    """
    user update form in wich user can update some of its data 
    """
    name = forms.CharField()
    surname = forms.CharField()
    date_of_birth = forms.DateField()
    tel = forms.CharField()
    
    class Meta:
        model = User
        fields = ["name", "surname", "date_of_birth", "tel"]


class SubjectUpdateForm(forms.ModelForm):
    """
    SubjectUpdate form is used to update subject name  and it short version
    to choose what subject will be changed/updated  is used function subject_name_choice
    """

    subject_to_change = forms.MultipleChoiceField(choices=subject_name_choices, widget= forms.CheckboxSelectMultiple,)
    subject_name = forms.CharField(help_text="New subject name")
    subject_short = forms.CharField(help_text="New subject short")
    
    class Meta:
        model = Subjects
        fields = ["subject_to_change", "subject_name", "subject_short"]

class ClassUpdateForm(forms.ModelForm):
    """
    form is used to update class 
    to choose what class will be changed/updated  is used class_choice
    """
    class_to_change = forms.MultipleChoiceField(choices=class_choices, widget= forms.CheckboxSelectMultiple,)
    class_name = forms.CharField(help_text="New class name")
    
    
    class Meta:
        model = Classes
        fields = ["class_to_change","class_name"]

class HRUserUpdateForm(forms.ModelForm):
    """
    this form is made directly for HR/admin worker using user_name_options function to choose wich user data will
    be changed and here are no limitations of change
    we can change email and role too
    """    
    update_data_for_user = forms.ChoiceField(choices=user_name_opions)
    user_level = forms.ChoiceField(choices= User.USER_LEVEL_CHOICES)
    name = forms.CharField()
    surname = forms.CharField()
    date_of_birth = forms.DateField()
    tel = forms.CharField()
    

    class Meta:
        model = User
        fields = ['update_data_for_user', 'user_level', 'name', 'surname', 'date_of_birth', 'tel' ]

"""ADVANCED REGISTRATION FORMS"""
class TeacherAdvanceRegister(forms.ModelForm):
    """
    this form comes automatically up after teacher registration to  register Teacher model and fill up additional data for teacher
    """
    user = forms.ChoiceField(choices=teacher_name_opions)
    subjects = forms.MultipleChoiceField(choices= subject_name_choices, widget= forms.CheckboxSelectMultiple, label='Taught Subjects:')
    classes = forms.MultipleChoiceField(choices= class_choices, widget= forms.CheckboxSelectMultiple, label='Teaching in:')
    
    class Meta:
        model = Teacher
        fields = ["user", "subjects","main_class", "classes"]

class StudentAdvanceRegister(forms.ModelForm):
    """
    this form comes automatically up after student registration to  register Student model and fill up additional data for teacher
    """
    user = forms.ChoiceField(choices=student_name_opions)
    subjects = forms.MultipleChoiceField(choices= subject_name_choices, widget= forms.CheckboxSelectMultiple)
    classes = forms.MultipleChoiceField(choices= class_choices, widget= forms.CheckboxSelectMultiple)

    class Meta:
        model = Student
        fields = ["user", "subjects", "classes", "activities", "parent_1", "parent_2"]

class ParentAdvanceRegister(forms.ModelForm):
    """
    this form comes automatically up after parent registration to  register Parentt model and fill up additional data for teacher
    """
    user = forms.ChoiceField(choices=parent_name_options)
    
    class Meta:
        model = Parent
        fields = ["user", "child"]

"""DELETE FORMS"""
class SubjectRemove(forms.ModelForm):
    """
    form that uses subject_name_choices function to pick and remove certain subject
    """
    subject_name = forms.ChoiceField(choices=subject_name_choices)

    class Meta:
        model = Subjects
        fields = ["subject_name"]

class ClassesRemove(forms.ModelForm):
    """
    form that uses class_choices function to pick and remove certain class
    """
    class_name = forms.ChoiceField(choices=class_choices)
    class Meta:
        model = Classes
        fields = ["class_name"]

class UserRemove(forms.ModelForm):
    """
    form that uses user_name_choices function to pick and remove certain user and everything connected to it
    """ 
    user = forms.ChoiceField(choices=user_name_opions)
    class Meta:
        model = User
        fields = ["user"]