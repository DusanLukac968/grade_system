from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("", views.MainPage.as_view(), name="main_page"),
    path('login_page/', views.LoginView.as_view(), name="login_page"),
    path('logout', views.logout_user, name= 'logout'),
    path('hr_register/', views.user_register, name= 'hr_register'),
    path('hr_workplace/', views.HrWorkplace.as_view(), name="hr_workplace"),
    path('subject_management/', views.SubjectManagement.as_view(), name="subject_management"),
    path('subject_add/', views.subject_add, name="subject_add"),
    path('subject_remove/', views.subject_remove, name="subject_remove"),
    path('user_remove/', views.user_remove, name="user_remove"),
    path('classes_management/', views.ClassesManagement.as_view(), name="classes_management"),
    path('classes_add/', views.classes_add, name="classes_add"),
    path('classes_remove/', views.classes_remove, name="classes_remove"),
    path('classes_update/',views.classes_update, name= "classes_update"),
    path('personal_and_student/', views.PersonalStudentsManagement.as_view(), name= "personal_and_student"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('user_update/',views.user_update, name= "user_update"),
    path('hr_user_update/',views.hr_user_update, name= "hr_user_update"),
    path('subject_update/',views.subject_update, name= "subject_update"),
    path('teacher_advance_register/',views.teacher_advance_register, name= "teacher_advance_register"),
    path('student_advance_register/',views.student_advance_register, name= "student_advance_register"),
    path('parent_advance_register/',views.parent_advance_register, name= "parent_advance_register"),
]