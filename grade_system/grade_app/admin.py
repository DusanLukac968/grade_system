from typing import Any
from django.contrib import admin
from django import forms
from .models import User, UserManager, Student, Teacher, Parent, Subjects, Classes 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget= forms.PasswordInput)

    class Meta:
        model = User
        fields = ["user_id","name", "surname", "date_of_birth", "tel", "email",]
    def save(self, commit = True):
        if self.is_valid():
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user



admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Subjects)
admin.site.register(Classes)
