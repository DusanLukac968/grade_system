from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date
from django.db.models.query import QuerySet
import uuid
from django.urls import reverse


class Subjects(models.Model):
    subject_name = models.CharField(max_length=300, unique=True)
    subject_short = models.CharField(max_length=300, unique=True)
    

    class Meta:
        verbose_name = "subject"   
        verbose_name_plural = "subjects"
    
    def __str__(self):
        return self.subject_short

class Classes(models.Model):
    class_name = models.CharField(max_length=300, unique=True)

    class Meta:
        verbose_name = "class"   
        verbose_name_plural = "classes"
    
    def __str__(self):
        return self.class_name

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        print(self)
        if email and password:
            user = self.model(email = self.normalize_email(email))
            user.set_password(password)
            user.save()
            return user
        
    def create_superuser(self, email, password):
        user = self.create_user( email, password)
        user.is_admin = True
        user.save()
        return user
    

class User(AbstractBaseUser):
    ADMIN = 0
    PRINCIPAL = 1
    TEACHER = 2
    STUDENT = 3
    PARENT = 4
    USER_LEVEL_CHOICES = (
        (ADMIN, "Admin"),
        (PRINCIPAL, "Principle"),
        (TEACHER, "Teacher"),
        (STUDENT, "Student"),
        (PARENT, "Parent"),
    )
    user_level = models.PositiveBigIntegerField(choices= USER_LEVEL_CHOICES, default=0 )
    user_id = models.UUIDField(primary_key= True,unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)
    surname = models.CharField(max_length=300)
    date_of_birth = models.DateField(max_length=8, default='1980-01-01')
    tel = models.CharField(max_length=12)
    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField('is_admin',default=False)


    class Meta:
        verbose_name = "user"   
        verbose_name_plural = "users"
    
    objects = UserManager()

    USERNAME_FIELD = "email"

    def get_full_name(self):
        return f"{self.name}  {self.surname}"

    def get_short_name(self):
        return self.name and self.surname or self.email.split('@')[0]

    def __str__(self):
        return "email: {0}\n name: {1}\n surname: {2}\n telephone number: {3}\n user_id: {4}\n user role: {5}".format(self.email, self.name, self.surname, self.tel, self.user_id, self.user_level)

    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True   



class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.UUIDField(primary_key= True,unique=True, default=uuid.uuid4, editable=False)
    subjects = models.ManyToManyField(Subjects,default="", verbose_name="Subjecs ")
    classes = models.ManyToManyField(Classes, default="", verbose_name="Classes")
    

    def __str__(self):
        return "User {0},\n teacher_id: {1}\n subjects: {2}\n Teacher class: {3}".format(self.user, self.teacher_id, self.subjects, self.classes)

    class Meta:
        verbose_name = "teacher"
        verbose_name_plural = "teachers"

    


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    subjects = models.ManyToManyField(Subjects,default="", verbose_name="Subjecs ")
    current_class = models.ManyToManyField(Classes, default="", verbose_name="Classes")
    activities = models.CharField(max_length=300)
    parent_1 = models.CharField(max_length=300)
    parent_2 = models.CharField(max_length=300)

    class Meta:
        verbose_name = "student"   
        verbose_name_plural = "students"


    def __str__(self):
        return "class: {0},\n user: {1}, student_id:{3}".format(self.current_class, self.user, self.student_id)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    child = models.CharField(max_length=300)

    class Meta:
        verbose_name = "parent"   
        verbose_name_plural = "parents"

    def __str__(self):
        return "user: {0}, child: {1}, surname: {2}".format(self.user, self.child)

