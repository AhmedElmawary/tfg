from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.shortcuts import get_object_or_404

from app.models import User
from app.serializers import AthleteSearchSerializer

from . import serializers
from .models import CoachNote
from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin

from rest_framework.authentication import TokenAuthentication
from app import permissions
#added by gerges 
from app import models as app_models
from app import serializers as app_serializers
from datetime import date
"""
For retreiving notes for Coach by id
"""


# class CoachNotes(viewsets.ViewSet):
#     permission_classes = (
#         permissions.LoggedInPermission,
#         permissions.IsStaff,
#         permissions.CoachOfNote,
#     )
#     authentication_classes = (TokenAuthentication,)

#     def retrieve(self, request, pk):
#         serializer_class = serializers.CoachNoteRetrieveSerializer
#         app_user = get_object_or_404(User, id=pk)
#         notes = app_user.coach_notes
#         # queryset = CoachNote.objects.filter(User=pk,)
#         queryset = notes
#         data = serializer_class(queryset, many=True).data

#         return Response({"data": data}, status=200)

#     def create(self, request):
#         data = request.data
#         _note = [data.get(key) for key in ["coach", "note"]]
#         user = data.get("user")
#         serializer_class = serializers.CoachNoteCreateSerializer
#         note = serializer_class(data=data)

#         if note.is_valid(raise_exception=True):
#             note = note.save()

#             if user:
#                 note_user = get_object_or_404(User, id=int(user))

#                 if not note_user.is_staff:
#                     note_user.coach_notes.add(note)
#                     note_user.save()
#                 else:
#                     return Response("You can't create note for a Coach.", status=400)

#             else:
#                 return Response("user field is requerd.", status=400)

#         return Response("You have created Your note.", status=201)


class AthleteSearch(APIView):
    permission_classes = (permissions.IsStaff,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        q = request.query_params.get("q")
        page_num = int(request.query_params.get("page", 1))
        users = User.objects.all()

        search_q = Q(Q(FirstName=q) | Q(SecondName=q))
        data = users.filter(search_q).filter(is_staff=False)

        paginator = Paginator(data, 1)

        try:
            paginator.page(page_num)
        except EmptyPage:
            return Response({"error": "This page doesn't exist!"}, status=404)

        page = paginator.page(page_num)

        next = (
            "{}?q={}&page={}".format(
                request.build_absolute_uri(reverse("CoachApp:AthleteSearch")),
                q,
                page.next_page_number(),
            )
            if page.has_next()
            else False
        )
        perv = (
            "{}?q={}&page={}".format(
                request.build_absolute_uri(reverse("CoachApp:AthleteSearch")),
                q,
                page.previous_page_number(),
            )
            if page.has_previous()
            else False
        )

        results = AthleteSearchSerializer(page, many=True).data

        payload = {
            "count": paginator.count,
            "next": next,
            "perv": perv,
            "results": results,
        }
        return Response(payload, status=200)


"""
this endpoint returns sessions that coach assigned to it with date greater than or equal today
"""
class CoachSessions(APIView):
    permission_classes = (permissions.IsStaff,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
                
            coach = self.request.user 
            today = date.today()
            coach_sessions = set(app_models.Session.objects.filter(coach=coach,dates__date__date__gte=today))
            serializer = app_serializers.CoachSessionSerializer
            data = serializer(coach_sessions,many=True).data
            return Response({"data":data},status=200)
        except Exception as e:
            return Response({"error":str(e)},status=400)
        

"""
this endpoint returns to coach specific session users 
"""
class SessionJoinedUsers(APIView):
    permission_classes = (permissions.IsStaff,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            users = []
            session = self.request.GET['session']
            date = self.request.GET['date']
            user_serializer = app_serializers.UserSerializer
            session_requests = app_models.SessionAttendanceRequest.objects.filter(
                session__id=int(session),
                date__id=date,
                joined=True,
                )
            session_requests_users = set([users.append(x.user) for x in session_requests if x.user not in users])
            data = user_serializer(users,many=True).data
            return Response({"data":data},status=200)
        except Exception as e:
            return Response({"error":str(e)},status=400)

"""
this endpoint returns and create and retrieve coach notes 
"""
class CoachNoteView(ViewSetMixin,generics.ListCreateAPIView):
    # queryset= 
    permission_classes = (permissions.IsStaff,)
    authentication_classes = (TokenAuthentication,)
    serializer_class =serializers.CoachNoteRetrieveSerializer
    
    def get_queryset(self):
        """Returns Polls that were created today"""
        return CoachNote.objects.filter(user__id=int(self.request.GET.get('user',1)))

    def create(self, request, *args, **kwargs):
        serializer_class =serializers.CoachNoteRetrieveSerializer
        request.data['coach']=request.user.id
        valid_data = serializer_class(data=request.data)
        if valid_data.is_valid():
            valid_data.save()
            user = app_models.User.objects.get(id=self.request.data['user'])
            user.coach_notes.add(valid_data.instance)
            user.save()
            return Response({"data":serializer_class(valid_data.instance).data})
        
        else:
            return Response({"error":valid_data.errors},status=400)