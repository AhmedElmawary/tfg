from rest_framework import serializers

from app.models import User
from app.serializers import UserSerializer, BasicPackageSerializer

from . import models


class CoachNoteRetrieveSerializer(serializers.ModelSerializer):
    coach_name = serializers.SerializerMethodField()
    class Meta:
        model = models.CoachNote
        fields = (
            "coach",
            "note",
            "timestamp",
            "coach_name"
        )
    def get_coach_name(self,obj):
        return obj.coach.FirstName
        # depth = 1


class CoachNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoachNote
        fields = (
            "coach",
            "note",
        )


class CoachNoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoachNote
        fields = (
            "id",
            "note",
        )
