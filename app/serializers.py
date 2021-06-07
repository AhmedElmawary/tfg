from rest_framework import serializers
from app import models
from datetime import datetime, timedelta, date, time


# sign up serializer
class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        # exclude = ('picture', )

    def create(self, validated_data):
        user = super(SignUpUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


# base user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = (
            "password",
            "password_reset_code",
            "user_permissions",
            "last_login",
            "is_superuser",
            "groups",
            "coach_notes",
        )


# base user serializer
class AthleteSearchSerializer(serializers.ModelSerializer):
    packages = serializers.SerializerMethodField("is_packages")

    def is_packages(self, obj):
        return BasicPackageSerializer(
            models.Package.objects.filter(user=obj), many=True
        ).data

    class Meta:
        model = models.User
        exclude = (
            "password",
            "password_reset_code",
            "user_permissions",
            "last_login",
            "is_superuser",
            "is_staff",
            "groups",
            "id",
        )

class SessionAterializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionAt
        fields = "__all__"
        depth = 1

# session serializer
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ("title",  "difficulty_level", "day", "session_at", "month")
        depth = 1
 

# coach app session serializer
class CoachSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ['id','title','description','dates']
        depth = 1

# session serializer
class CommingSessionSerializer(serializers.ModelSerializer):
    dates = serializers.SerializerMethodField()

    class Meta:
        model = models.Session
        fields = ("id", "title", "description", "comments", "coach", "dates")
        depth = 1

    def get_dates(self, obj):
        today = date.today()
        if obj:
            return SessionDatesSerializer(
                obj.dates.filter(date__gte=today), many=True
            ).data
        else:
            return []


# boolean session  serializer : returns if user went to this session or not
class BooleanSessionSerializer(serializers.ModelSerializer):
    attended = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()

    class Meta:
        model = models.Session
        fields = ("id", "title", "description", "comments", "attended", "joined")
        depth = 1

    def get_attended(self, obj):
        if obj:
            session_date = int(self.context["session_date_id"])
            user_id = int(self.context["user_id"])
            attendance = models.SessionAttendanceRequest.objects.filter(
                session=obj, user__id=user_id, date__id=session_date, attended=True
            )
            if len(attendance) > 0:
                return True
            else:
                return False
        return False

    def get_joined(self, obj):
        if obj:
            session_date = int(self.context["session_date_id"])
            user_id = int(self.context["user_id"])
            attendance = models.SessionAttendanceRequest.objects.filter(
                session=obj, user__id=user_id, date__id=session_date, joined=True
            )
            if len(attendance) > 0:
                return True
            else:
                return False
        return False


# session  attendance serializer
class SessionAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionAttendanceRequest
        exclude = ("package", "user")
        depth = 1


# SessionDatesSerializer
class SessionDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionDates
        fields = "__all__"


#  SessionComments
class SessionCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionComments
        fields = "__all__"


# session class serializer
# class SessionClassSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.SessionClass
#         fields = '__all__'


# package serializer
class BasePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = (
            "title",
            "description",
            "price",
            "period",
            "currency",
            "start_date",
            "end_date",
        )


# basic package serializer
class BasicPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        exclude = ("user", "sessions")


# details package serializer
class PackageSerializer(serializers.ModelSerializer):
    sessions = serializers.SerializerMethodField()

    class Meta:
        model = models.Package
        # fields = '__all__'
        exclude = ("user",)
        extra_fields = ["sessions"]

    # to not override all fields names one by one in fields
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(PackageSerializer, self).get_field_names(
            declared_fields, info
        )
        if getattr(self.Meta, "extra_fields", None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    # ____________________________________________________
    def get_sessions(self, obj):
        if obj:
            sessions = SessionSerializer(obj.sessions, many=True).data
            return sessions
        else:
            return []


# package category serializer
class PackageCategorySerializer(serializers.ModelSerializer):
    packages = serializers.SerializerMethodField()

    class Meta:
        model = models.PackageCategory
        fields = ("title", "picture", "packages")

    def get_packages(self, obj):
        if obj:
            package = BasicPackageSerializer(obj.packages, many=True).data
            return package
        else:
            return []


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GeneralInfo
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = "__all__"
