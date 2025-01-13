from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("", views.MainPage.as_view(), name="main_page"),
    path('login_page/', views.LoginView.as_view(), name="login_page"),
    path('logout', views.logout_user, name= 'logout'),
    path('hr_register/', views.hr_register, name= 'hr_register'),
    path('teacher_register_page/', views.teacher_register, name= 'teacher_register_page'),
    path('hr_workplace/', views.HrWorkplace.as_view(), name="hr_workplace"),
    path('student_register_page/', views.student_register, name="student_register_page"),
    path('subject_management/', views.SubjectManagement.as_view(), name="subject_management"),
    path('subject_add/', views.subject_add, name="subject_add"),
    path('subject_remove/', views.subject_remove, name="subject_remove"),
    path('classes_management/', views.ClassesManagement.as_view(), name="classes_management"),
    path('classes_add/', views.classes_add, name="classes_add"),
    path('classes_remove/', views.classes_remove, name="classes_remove"),
    path('personal_and_student/', views.PersonalStudentsManagement.as_view(), name= "personal_and_student"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('user_update/',views.user_update, name= "user_update"),
    path('hr_teacher_advance_register/',views.hr_teacher_advance_register, name= "hr_teacher_advance_register"),
    path('teacher_advance_register/',views.teacher_advance_register, name= "teacher_advance_register"),
    path('test/', views.TeacherAdvanceRegisterI.as_view(), name="test")
]