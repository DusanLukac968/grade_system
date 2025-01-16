from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Student, Teacher, Subjects, Classes
from .forms import LoginForm, UserRegistrationForm, TeacherRegistrationForm, StudentRegistrationForm, SubjectAdd, ClassesAdd, SubjectRemove,ClassesRemove, UserUpdateForm, TeacherAdvanceRegister

class MainPage(generic.ListView):

    template_name = "grade_system/main_page.html"
    context_object_name = "main_page"

    def get_queryset(self):
        return User.objects.all().order_by("-user_id")
    
class LoginView(generic.edit.CreateView):
    """
    view for HR/staff login 
    special login after login changes colour of webpage to staff colour acess to staff profile 
    """

    form_class = LoginForm
    template_name = 'grade_system/login_page.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"{user.email} succesfully logged in :)")
                return redirect("main_page")
            else:
                messages.error(request, "Something went wrong!")
        return render(request, self.template_name, {"form": form})


class HrWorkplace(generic.TemplateView):

    template_name = "grade_system/hr_workplace.html"
    context_object_name = "hr_workplace"

class SubjectManagement(generic.ListView):
    template_name = "grade_system/subject_management.html"
    context_object_name = "subject_management"

    def get_queryset(self):
        return Subjects.objects.all().order_by("subject_short")
    
class ClassesManagement(generic.ListView):
    template_name = "grade_system/classes_management.html"
    context_object_name = "classes_management"

    def get_queryset(self):
        return Classes.objects.all().order_by("class_name")

class PersonalStudentsManagement(generic.TemplateView):

    template_name = "grade_system/personal_and_students.html"
    content_object_name = "personal_and_student"


def hr_register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f"Account for HR {email} was created.")
            return redirect('main_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'grade_system/user_register.html', { 'form': form}) 

def teacher_register(request):
    
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            messages.success(request, f"Account for teacher {name} {surname}")
            return redirect('teacher_advance_register')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'grade_system/teacher_register_page.html', { 'form': form})

def student_register(request):
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            messages.success(request, f"Account for Student {name} {surname}")
    else:
        form = StudentRegistrationForm()
    return render(request, 'grade_system/student_register_page.html', { 'form': form})


def subject_add(request):
    
    if request.method == 'POST':
        form = SubjectAdd(request.POST)
        if form.is_valid():
            form.save()
            subject_name = form.cleaned_data.get('subject_name')
            subject_short = form.cleaned_data.get('subject_short')
            messages.success(request, f"New subject {subject_name} : {subject_short} added. ")
            return redirect('hr_workplace')
    else:
        form = SubjectAdd()
    return render(request, 'grade_system/subject_add.html', { 'form': form})

def subject_remove(request):
        
    if request.method == 'POST':
        form = SubjectRemove(request.POST)
        subject_name = request.POST.get('subject_name')
        try:
            if form.is_valid():
                remove_this_subject = Subjects.objects.get(pk= subject_name)
                remove_this_subject.delete()
                messages.success(request,f"Subject {remove_this_subject.subject_name} has been deleted!")
                return redirect('hr_workplace')
        except Subjects.DoesNotExist:
            messages.error(request,f"Subject{subject_name} does not exist!")
            return redirect('hr_workplace')      
    else:
        form = SubjectRemove()
    return render(request, 'grade_system/subject_remove.html', { 'form': form})

def classes_add(request):
    
    if request.method == 'POST':
        form = ClassesAdd(request.POST)
        if form.is_valid():
            form.save()
            class_name = form.cleaned_data.get('class_name')
            messages.success(request, f"New class {class_name} added. ")
            return redirect('hr_workplace')
    else:
        form = ClassesAdd()
    return render(request, 'grade_system/classes_add.html', { 'form': form})

def classes_remove(request):
    if request.method == 'POST':
        form = ClassesRemove(request.POST)
        class_name = request.POST.get('class_name')
        try:
            if form.is_valid():
                remove_this_class = Classes.objects.get(pk= class_name)
                remove_this_class.delete()
                messages.success(request, f"Class {remove_this_class.class_name} has been deleted!")
                return redirect('hr_workplace')
        except Classes.DoesNotExist:
            messages.error(request,f"Class {class_name} does not exist!" )
            return redirect('hr_workplace')
    else:
        form = ClassesRemove()
    return render(request, 'grade_system/classes_remove.html', {'form': form})

def logout_user(request):
    """
    allows user to logout and redirect him to the main page
    """
    logout(request)
    messages.success(request, "succesfully logged out")
    return redirect("main_page")

@login_required
def user_profile(request):

    user = get_user_model()
    if user:
        return render(request, 'grade_system/user_profile.html' )
    return redirect("main_page")

@login_required
def user_update(request):

    if request.method == 'POST':
        user = get_user_model()
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request,f'{user_form}, has been updated!')
            return redirect('user_profile')
        """ add some errors"""
    user = get_user_model()
    if user:
        form = UserUpdateForm(instance=request.user)
        return render(request, 'grade_system/user_update.html', {'form': form})
    return redirect("user_profile")


@login_required
def hr_teacher_advance_register(request):
    if request.method == 'POST':
        form = TeacherAdvanceRegister(request.POST)
        user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, f"Account was created.")
            return redirect('main_page')
    else:
        form = TeacherAdvanceRegister()
    return render(request, 'grade_system/hr_workplace.html', { 'form': form}) 

@login_required
def teacher_advance_register(request):

    if request.method == 'POST':
        form = TeacherAdvanceRegister(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, f"Account was created.")
                return redirect('main_page')
            
        except:
            pass
    else:
        form = TeacherAdvanceRegister()
    return render(request, 'grade_system/user_register.html', { 'form': form}) 
