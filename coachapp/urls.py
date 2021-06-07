from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("CoachNoteView", views.CoachNoteView,basename='CoachNoteView')

urlpatterns = [
    path("", include(router.urls)),
    path("Athletes/", views.AthleteSearch.as_view(), name="AthleteSearch"),
    path("CoachSessions/", views.CoachSessions.as_view(), name="CoachSessions"),
    path("SessionJoinedUsers/", views.SessionJoinedUsers.as_view(), name="SessionJoinedUsers"),
    
    
]
