from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Student, Teacher, Subjects, Classes, Parent
from .forms import LoginForm, UserRegistrationForm, SubjectAdd, ClassesAdd, SubjectRemove,ClassesRemove, UserUpdateForm, TeacherAdvanceRegister, StudentAdvanceRegister, SubjectUpdateForm, ClassUpdateForm, HRUserUpdateForm, ParentAdvanceRegister, UserRemove, GiveGrade

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


def user_register(request):
    """
    user registration view for user registration using UserRegistrationForm
    creating new user 
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            user_level = form.cleaned_data.get('user_level')
            if int(user_level) == 2:
                messages.success(request, f"Account for Teacher {email} was created.")
                return redirect('teacher_advance_register')
            elif int(user_level) == 3:
                messages.success(request, f"Account for student {email} was created.")
                return redirect('student_advance_register')
            elif int(user_level) == 4:
                messages.success(request, f"Account for parent {email} was created.")
                return redirect('parent_advance_register')
            elif int(user_level) == 0:
                messages.success(request, f"Account for new colleague {email} was created.")
                return redirect('hr_workplace')           
    else:
        form = UserRegistrationForm()
    return render(request, 'grade_system/user_register.html', { 'form': form}) 



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

@login_required
def user_remove(request):
    """view for deleting users"""
    if request.method == 'POST':
        form = UserRemove(request.POST)
        get_user = request.POST.get('user')
        remove_this_user = User.objects.get(pk = get_user)
        try:
            if form.is_valid():
                if int(remove_this_user.user_level) == 2:
                    user_teacher_to_delete = Teacher.objects.get(user = get_user)
                    user_teacher_to_delete.delete()
                elif int(remove_this_user.user_level) == 3:
                    user_student_to_delete = Student.objects.get(user = get_user)
                    user_student_to_delete.delete()
                elif int(remove_this_user.user_level) == 4:
                    user_parent_to_delete = Parent.objects.get(user = get_user)
                    user_parent_to_delete.delete()
                remove_this_user.delete()
                messages.success(request, f"User {remove_this_user.name} {remove_this_user.surname} and all connected data has been deleted!")
        except User.DoesNotExist:
            messages.error(request,f"Class {get_user} does not exist!" )
            return redirect('hr_workplace')
    else:
        form = UserRemove()
    return render(request, 'grade_system/user_remove.html', {'form': form})

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
            messages.success(request,'Your profile has been updated!')
            return redirect('user_profile')
        """ add some errors"""
    user = get_user_model()
    if user:
        form = UserUpdateForm(instance=request.user)
        return render(request, 'grade_system/user_update.html', {'form': form})
    return redirect("user_profile")


class HrUserEdit(generic.edit.CreateView):
    form_class = HRUserUpdateForm
    template_name = 'grade_system/hr_user_update.html'

    
    def get(self, request, pk):        
        if not request.user.user_level == 0:
            messages.info(request, "You are not obligated to enter this page!")
            return redirect("main_page")
        try:
            user = User.objects.get(pk = pk)
        except:
            messages.error(request, "This user doesn't exist")
            return redirect("main_page")
        form = self.form_class(instance = user)
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, pk):
        if not request.user.user_level == 0:
            messages.info/request, "You are not obligated to enter this page!"
            return redirect("main_page")
        form = self.form_class(request.POST)

        if form.is_valid():
            user_level = form.cleaned_data["user_level"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            tel = form.cleaned_data["tel"]
            try:
                user = User.objects.get(pk = pk)
                old_level = user.user_level
            except:
                messages.error(request, "User doesn't exist")
                return redirect("main_page")
            user.user_level = user_level
            user.name = name
            user.surname = surname
            user.date_of_birth = date_of_birth
            user.tel = tel
            user.save()
            if old_level != user.user_level:
                if old_level == 2:
                    get_teacher = Teacher.objects.get(user = user)
                    try:
                        get_teacher.delete()
                        messages.success(request, f"Teacher profile for user {user.name} {user.surname} deleted continue to new register")
                        if int(user.user_level) == 3:
                            return redirect("student_advance_register")
                        elif int(user.user_level) == 4:
                            return redirect("parent_advance_register")
                    except Teacher.DoesNotExist:
                        messages.error(request, "1Somthing went wrong :(")
                elif old_level == 3:
                    get_student = Student.objects.get(user = user)
                    try:
                        get_student.delete()
                        messages.success(request, f"Student profile for user {user.name} {user.surname}  deleted continue to new register")
                        if int(user.user_level) == 2:
                            return redirect("teacher_advance_register")
                        elif int(user.user_level) == 4:
                            return redirect("parent_advance_register")
                    except Student.DoesNotExist:
                        messages.error(request, f"Somthing went wrong :(")
                elif old_level == 4:
                    get_parent = Student.objects.get(user = user)
                    try:
                        get_parent.delete()
                        messages.success(request, f"Parents profile for user {user.name} {user.surname} deleted continue to new register")
                        if int(user.user_level)==3:
                            return redirect("student_advance_register")
                        elif int(user.user_level)==2:
                            return redirect("teacher_advance_register")
                    except Parent.DoesNotExist:
                        messages.error(request, "3Somthing went wrong :(")
                else:
                    pass
                    """ I have to make change in same user levels"""
        return render(request, self.template_name, {"form": form})
  
class UserIndex(generic.ListView):
    template_name = "grade_system/user_index.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()
    

class UserProfiles(generic.DetailView):

    model = User
    template_name = "grade_system/user_details.html"

    def get(self, request, pk):
        try:
            user = self.get_object()
        except:
            return redirect("user_index")
        return render(request, self.template_name, {"user": user})
    
    def post(self, request, pk):
        if request.user.user_level == 0:
            if "edit" in request.POST:
                return redirect("hr_user_edit", pk = self.get_object().pk)
            else:
                if not request.user.user_level == 0:
                    messages.info(request, "You can't do that!")
                    return redirect("user_index")
                else:
                    self.get_object().delete()
        return redirect("user_index")

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

@login_required
def parent_advance_register(request):
    """
    view for student registration to user with user_role student allows us to specify additional data 
    """
    if request.method == 'POST':
        form = ParentAdvanceRegister(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, f"Account was created.")
                return redirect('main_page')
            
        except:
            pass
    else:
        form = ParentAdvanceRegister()
    return render(request, 'grade_system/user_register.html', { 'form': form}) 

@login_required
def give_grade(request):
    """
    view in which we can add grade to student
    """
    if request.method == 'POST':
        form = GiveGrade(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"New subject added. ")
            return redirect('hr_workplace')
    else:
        form = GiveGrade()
    return render(request, 'grade_system/give_grade.html', { 'form': form})
