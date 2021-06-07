from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from unique_upload import unique_upload
from django import forms
import datetime
from coachapp import models as coach_models
from django.utils.crypto import get_random_string

""" upload function """


def file_upload(instance, filename):
    return unique_upload(instance, filename)


""" 
main user model 
"""


class UserManager(BaseUserManager):
    """"Helps handle Users"""

    def create_user(self, password, email, **kyargs):
        if not email:
            raise ValueError("Must have an email")

        email = self.normalize_email(email)
        newUser = self.model(email=email, **kyargs)
        newUser.set_password(password)
        newUser.save(using=self._db)
        return newUser

    def create_superuser(self, email, password=None):
        newSuperUser = self.create_user(password, email,)
        newSuperUser.is_superuser = True
        newSuperUser.is_staff = True
        newSuperUser.set_password(password)
        newSuperUser.save(using=self._db)
        return newSuperUser


# App user
class User(AbstractBaseUser, PermissionsMixin):

    FirstName = models.CharField(max_length=300)
    SecondName = models.CharField(max_length=300, blank=True, null=True,default="no_last_name")
    profile_pic = models.ImageField(upload_to=file_upload, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    password_reset_code = models.CharField(max_length=10, null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    key = models.CharField(
        default=get_random_string, max_length=500, unique=True, blank=True, null=True
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    coach_notes = models.ManyToManyField("coachapp.CoachNote", blank=True, null=True)
    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return str(self.FirstName) + "_" + str(self.SecondName) or str(self.FirstName)


"""
PACKAGE CATEGORY
"""


class PackageCategory(models.Model):
    packages = models.ManyToManyField(
        "Package", related_name="packages", blank=True, null=True
    )
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to=file_upload, blank=True, null=True)

    def __str__(self):
        return str(self.title)


"""
Package
"""


class Package(models.Model):
    user = models.ManyToManyField(
        "User", related_name="active_user", blank=True, null=True
    )
    # adding table in DB by name app > package > deactivated_users
    deactivated_users = models.ManyToManyField(
        "User", related_name="deactivated_users_name", blank=True
    )
    # adding table in DB by name app > package > sessions
    sessions = models.ManyToManyField(
        "Session", related_name="sessions", blank=True, null=True
    )
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    yearly_price = models.FloatField(default=1.0)
    period = models.CharField(
        max_length=200, choices=(
            ("Month", "Month"),
            ("sessions", "sessions only"), 
            ("3months", "3months"),
            ("endless", "endless")
        ), default="Month"
    )
    currency = models.CharField(max_length=200, default="EGP")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


"""
Sessions 
"""


class SessionDates(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return str(self.date)


class SessionComments(models.Model):
    title = models.TextField()

    def __str__(self):
        return str(self.id)

class DifficultyLevel(models.Model):
    name = models.CharField(max_length=250)

class SessionDay(models.Model):
    name = models.CharField(max_length=250)

class SessionAt(models.Model):
    at = models.TimeField()


class SessionMonth(models.Model):
    name = models.CharField(max_length=250)



class Session(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    coach = models.ForeignKey(
        "User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="session_coach",
    )
    
    # dates = models.ManyToManyField(
    #     "SessionDates", blank=True, related_name="_SessionDates"
    # )

    session_at = models.OneToOneField(
        SessionAt,  null=True,on_delete=models.SET_NULL
    )

    comments = models.ManyToManyField(
        "SessionComments", blank=True, related_name="_SessionComments"
    )
    difficulty_level = models.ManyToManyField(DifficultyLevel)
    day = models.ManyToManyField(SessionDay)
    month = models.ManyToManyField(SessionMonth)

    # users = models.ManyToManyField('User',blank=True,null=True,related_name='attendees')
    # classes = models.ManyToManyField('SessionClass',blank=True,null=True,related_name='session_classes')
    # max_seats = models.IntegerField(default=1)
    # current_seats = models.IntegerField(default=0)
    def __str__(self):
        return str(self.title)


class SessionAttendanceRequest(models.Model):
    user = models.ForeignKey(
        "User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="session_user",
    )
    coach = models.ForeignKey(
        "User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="session_attendance_coach",
    )
    session = models.ForeignKey(
        "Session",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="_session",
    )
    package = models.ForeignKey(
        "Package",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="package",
    )
    date = models.ForeignKey(
        "SessionDates",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="session_date",
    )
    attended = models.BooleanField(default=False)
    joined = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


"""
sessions Classes 
"""
# class SessionClass(models.Model):
#     title = models.CharField(max_length=300)
#     description = models.TextField()

#     start_date = models.DateTimeField(default=datetime.datetime.now,blank=True,null=True)
#     end_date = models.DateField(default=datetime.date.today,blank=True,null=True)

#     def __str__(self):
#         return str(self.title)


"""
attendance 
"""


class Attendance(models.Model):
    user = models.ForeignKey(
        "User",
        related_name="attendance_user",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    coach = models.ForeignKey(
        "User",
        related_name="attendance_coach",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    package = models.ForeignKey(
        "Package",
        related_name="Package_attendance",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    date = models.DateField(auto_now=True)
    session = models.ForeignKey(
        "Session",
        related_name="attendance_session",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    # session_class = models.ForeignKey('SessionClass',related_name='attendance_class_session',blank=True,null=True,on_delete=models.SET_NULL)
    direction = models.CharField(max_length=20, blank=True, null=True, default="in")
    from_gates = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


"""
info model
"""


class GeneralInfo(models.Model):
    text = models.TextField()
    Choices = (
        ("About", "About"),
        ("Rules", "Rules"),
    )
    info_type = models.CharField(max_length=20, choices=Choices)


"""
FAQ MODEL
"""


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return str(self.question)


"""
    schedule model
"""
class Schedule(models.Model):
    test = models.CharField(max_length=20, null=True)
    # month = models.CharField(max_length=20, null=True)
    # workout = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.id)
