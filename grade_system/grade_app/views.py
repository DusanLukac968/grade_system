from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Student, Teacher, Subjects, Classes
from .forms import LoginForm, UserRegistrationForm, TeacherRegistrationForm, StudentRegistrationForm, SubjectAdd, ClassesAdd, SubjectRemove,ClassesRemove, UserUpdateForm, TeacherAdvanceRegister, StudentAdvanceRegister, SubjectUpdateForm, ClassUpdateForm, HRUserUpdateForm

class MainPage(generic.ListView):
    """
    view of main page (not finished yet)
    """

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
    """
    HR workplace is view with option how to add/ remove/ update users as teacher students and subject classes
    """
    template_name = "grade_system/hr_workplace.html"
    context_object_name = "hr_workplace"

class SubjectManagement(generic.ListView):
    """
    view in which Hr can choose what to do with subjects
    add or remove them
    """
    template_name = "grade_system/subject_management.html"
    context_object_name = "subject_management"

    def get_queryset(self):
        return Subjects.objects.all().order_by("subject_short")
    
class ClassesManagement(generic.ListView):
    """
    view in which Hr can choose what to do with classes
    add or remove them
    """
    template_name = "grade_system/classes_management.html"
    context_object_name = "classes_management"

    def get_queryset(self):
        return Classes.objects.all().order_by("class_name")

class PersonalStudentsManagement(generic.TemplateView):
    """
    view in which Hr can choose what to do with students
    add or remove them
    """
    template_name = "grade_system/personal_and_students.html"
    content_object_name = "personal_and_student"


def hr_register(request):
    """
    user registration view for user registration using UserRegistrationForm
    creating new user 
    """
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
    """
    user registration view for user registration using TeacherRegistrationForm
    creating new user with fixed role teacher after creatin user, Hr is redirected to teacher_advance_register
    when full registration of teacher can be finished
    """  
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
    """
    user registration view for user registration using StudentRegistrationForm
    creating new user with fixed role teacher after creatin user, Hr is redirected to student_advance_register
    when full registration of student can be finished
    """    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            messages.success(request, f"Account for Student {name} {surname}")
            return redirect('student_advance_register')
    else:
        form = StudentRegistrationForm()
    return render(request, 'grade_system/student_register_page.html', { 'form': form})


def subject_add(request):
    """
    view in which we can add subject
    """
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
    """
    view in which we can remove subject
    """
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
    """
    view in which we can add class
    """   
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
    """
    view in which we can remove class
    """
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
    """
    view allows logged user to see user profile with option to jumt to user update view
    """
    user = get_user_model()
    if user:
        return render(request, 'grade_system/user_profile.html')
    return redirect('user_login')
        

@login_required
def user_update(request):
    """
    view in which user can update some of its data
    """
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
def hr_user_update(request):
    """
    view for HR/admin in which  can be updated all data for selected user
    """
    if request.method == 'POST':
        get_user = request.POST.get('update_data_for_user')
        user = User.objects.get(pk = get_user)
        form = HRUserUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect()
    user = get_user_model()
    if user:
        form = HRUserUpdateForm(instance=request.user)
        return render(request, 'grade_system/user_update.html', {'form': form})
    return redirect("hr_workplace")

@login_required
def subject_update(request):
    """
    view in which subject can be updatede/changed
    """
    if request.method == 'POST':
        get_subject= request.POST.get('subject_to_change')
        get_new_subject_name = request.POST.get('subject_name')
        get_new_subject_short = request.POST.get('subject_short')
        update_this_subject = Subjects.objects.get(pk= get_subject)
        form = SubjectUpdateForm(request.POST, instance=update_this_subject)
        if form.is_valid():
            update_this_subject.subject_name = get_new_subject_name
            update_this_subject.subject_short = get_new_subject_short
            update_this_subject.save()
            messages.success(request,f'Subject"{get_subject}" has been updated to "{get_new_subject_name}"!')
            return redirect('subject_update')
        """ add some errors"""
    user = get_user_model()
    if user:
        form = SubjectUpdateForm()
        return render(request, 'grade_system/subject_update.html', {'form': form})
    return redirect("subject_update")

@login_required
def classes_update(request):
    """
    view in which class can be updatede/changed
    """
    if request.method == 'POST':
        get_class = request.POST.get('class_to_change')
        get_new_class_name = request.POST.get('class_name')
        update_this_class = Classes.objects.get(pk = get_class)
        form = ClassUpdateForm(request.POST, instance=update_this_class)
        if form.is_valid():
            update_this_class.class_name = get_new_class_name
            update_this_class.save()
    
    if True:
        form = ClassUpdateForm()
        return render(request, 'grade_system/classes_update.html', {'form': form} )
   
@login_required
def teacher_advance_register(request):
    """
    view for teacher registration to user with user_role teacher allows us to specify additional data 
    """
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

@login_required
def student_advance_register(request):
    """
    view for student registration to user with user_role student allows us to specify additional data 
    """
    if request.method == 'POST':
        form = StudentAdvanceRegister(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, f"Account was created.")
                return redirect('main_page')
            
        except:
            pass
    else:
        form = StudentAdvanceRegister()
    return render(request, 'grade_system/user_register.html', { 'form': form}) 
