from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from app import serializers
from app import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.
from hashlib import sha256
from datetime import datetime, timedelta, date, time
from app import models
from app import serializers
from django.utils import timezone
from AcceptPaymentApp import models as accept_models

""" Userviews """


class UserViews(APIView):
    permission_classes = (permissions.UserViewsPermissions,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        request = self.request
        serializer = serializers.SignUpUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            return Response(
                {
                    "status": "created successfully",
                    "token": Token.objects.create(user=user).key,
                    "key": user.key,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        usr = self.request.user
        serializer = serializers.SignUpUserSerializer(
            usr, data=self.request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response({"status": "Updated successfully"}, status=200)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


""" login """


class LogInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        user_serializer = serializers.UserSerializer
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_data = user_serializer(user).data
        try:
            user_package = models.Package.objects.get(user=user)
            have_package = True
        except models.Package.DoesNotExist:
            have_package = False

        return Response(
            {"token": token.key, "user": user_data, "have_package": have_package},
            status=200,
        )


""" user rasspberry pass views
    User pass if he have un ended paid and activated payment 
"""


class SessionPassView(APIView):
    def post(self, request):
        try:
            key = self.request.data["key"]
            direction = self.request.data["direction"]
            day = datetime.now().date()
            user = models.User.objects.get(key=key)
            allow = False
            # pass him if direction is out 
            if direction == "out":
                attend, new = models.Attendance.objects.get_or_create(
                    user=user, date=day, direction=direction, from_gates=True
                )
                data = serializers.UserSerializer(user).data
                return Response({"status": True, "data": data}, status=200)

            payment = accept_models.Payment.objects.filter(
                end_date__gte=date.today(), user=user, paid=True, deactivated=False
            )
            
            attend, new = models.Attendance.objects.get_or_create(
                user=user, date=day, direction=direction, from_gates=True
            )
            data = serializers.UserSerializer(user).data

            ## deduct and  from user package sessions when he pass and check if he completed his sessions
            package = models.Package.objects.filter(user=user).first()
            if package.period =="endless":
                attended_sessions = models.SessionAttendanceRequest.objects.filter(user=user,package=package,attended=True)
                # compare attended sessions with package sessions
                if attended_sessions.count() >= package.sessions.count():
                    "add user to deactivated users of this package"
                    today = date.today()
                    package_deactivition = package.deactivated_users.add(user)
                    package_deactivition = package.user.remove(user)
                    payment = accept_models.Payment.objects.get(
                        user=user,
                        Subscription=package,
                        paid=True,
                        end_date__gte=today,
                        deactivated=False,
                    )
                    payment.deactivated = True
                    payment.save() 
                    return Response({"error":"sorry you consumed your all sessions"},status=400)

                else:    
                    deduction = models.SessionAttendanceRequest.objects.create(
                        user=user,
                        package=package,
                        attended=True,
                        joined=True
                        )
                                   


            if len(payment) > 0:
                allow = True
                # overriding bacause of request status code 
                return Response({"status": allow, "data": data}, status=200)
            else:
                return Response({"status": allow, "data": data}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


"""
coach deduct session for user 
"""


class CoachSessionPassView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsStaff,)

    def post(self, request):
        try:
            key = self.request.data["key"]
            session_id = self.request.data["session"]
            session_date = self.request.data["session_date"]
            # session max seats validation
            session = models.Session.objects.get(id=session_id)
            session_date = models.SessionDates.objects.get(id=session_date)
            # if not session.users.count()< session.max_seats:
            #     return Response({"error":"Sorry this session got max seats!"},status=400)
            # _________end of session validation __________
            user = models.User.objects.get(key=key)
            package = models.Package.objects.get(user=user)
            payment = accept_models.Payment.objects.filter(
                end_date__gte=date.today(),
                Subscription=package,
                user=user,
                paid=True,
                deactivated=False,
            )
            allow = False
            # ______ payment validation_______#
            if payment.count() > 0:
                day = datetime.now().date()
                direction = "In"
                # session attending assigning
                (
                    session_request,
                    new,
                ) = models.SessionAttendanceRequest.objects.get_or_create(
                    user=user,
                    coach=self.request.user,
                    session=session,
                    date=session_date,
                    package=package,
                    attended=True,
                )
                attend, new = models.Attendance.objects.get_or_create(
                    user=user,
                    date=day,
                    direction=direction,
                    coach=self.request.user,
                    session=session,
                )
                allow = True
            data = serializers.UserSerializer(user).data
            return Response({"status": allow, "data": data}, status=200)
        except Exception as e:
            raise
            return Response({"error": str(e)}, status=400)


"""
packages category view 
- retrieve all categories paginated
"""


# class PackagesCategoryView(generics.ListAPIView):
class PackagesCategoryView(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.LoggedInPermission,)
    def get(self, request):
        serializer_class = serializers.PackageCategorySerializer
        packeges_category = models.PackageCategory.objects.all()
        data = serializer_class(packeges_category, many=True).data
        return Response(data)

"""
my package view
"""


class MyPackageView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.LoggedInPermission,)

    def get(self, request):
        try:
            serializer_class = serializers.BasePackageSerializer
            user_serializer_class = serializers.UserSerializer
            # _____package filteration____#
            user = self.request.user
            package = models.Package.objects.get(user=user.id)
            # ____ remaining sessions _______#
            package_sessions_count = package.sessions.count()
            user_attended_sessions = models.SessionAttendanceRequest.objects.filter(
                user=user, package=package, attended=True
            ).count()
            remainging_sessions = package_sessions_count - user_attended_sessions
            if remainging_sessions < 0:
                remainging_sessions = 0

            try:
                # _____ payment part ______#
                payment = accept_models.Payment.objects.get(
                    Subscription=package,
                    user=self.request.user,
                    paid=True,
                    deactivated=False,
                )
                payment_expiry = payment.end_date
                date_a = datetime.today().date()
                date_b = payment_expiry
                time_difference = date_a - date_b
                time_difference = time_difference.days
                if time_difference > 0:
                    time_difference = 0
            except accept_models.Payment.DoesNotExist:
                payment_expiry = None
                time_difference = None
            # _____response part___________#
            if package:
                data = serializer_class(package).data
                return Response(
                    {
                        "package": data,
                        "user": user_serializer_class(self.request.user).data,
                        "payment_expiry": payment_expiry,
                        "time_difference": time_difference,
                        "remainging_sessions": remainging_sessions,
                    },
                    status=200,
                )
            else:
                return Response({"data": "No data packages found!"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)




"""
    ScheduleSession
"""

class ScheduleSession(APIView):
        def get(self, request):
            day = request.query_params["day"]
            month = request.query_params["month"]
            day_month = day+'-'+month
            datetime_object = datetime.strptime(day_month+"-2020", "%a-%b-%Y")
            # test = datetime.strftime(datetime_object, "%Y-%m-%d %H:%M:%S")
            day = models.SessionDay.objects.get(name=day)
            month = models.SessionMonth.objects.get(name=month)
            # test1 = day.session_set.all()            
            session_object = models.Session.objects.filter(day__id=day.id, month__id = month.id)  
            serializer = serializers.SessionSerializer
            result_json = serializer(session_object, many=True).data

            return Response(result_json,status=200)



"""
Today and all sessions 
"""


class UserPlanSessions(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.LoggedInPermission,)

    def get(self, request):
        try:
            user = self.request.user
            plan_sessions = models.Package.objects.filter(user=user)
            if plan_sessions.count() == 0:
                return Response({"error": "You dont have plans right now!"}, status=404)
            data = plan_sessions[0].sessions
            serializer = serializers.CommingSessionSerializer
            comming_data = serializer(data, many=True).data
            return Response({"comming_sessions": comming_data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


"""
return single session data by id(Get),join session by user(POST)
"""


class SingleSessionDataView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.LoggedInPermission,)

    def get(self, request):
        try:
            session_id = self.request.GET.get("session_id")
            session_date_id = self.request.GET.get("session_date_id")
            user = self.request.user
            sessions = models.Session.objects.filter(
                id=int(session_id), dates__id=int(session_date_id)
            )

            # check if user attended the session inside the serializer
            data = serializers.BooleanSessionSerializer(
                sessions,
                context={"session_date_id": session_date_id, "user_id": user.id},
                many=True,
            ).data
            date_result = models.SessionDates.objects.get(id=session_date_id)
            date_result = serializers.SessionDatesSerializer(date_result).data
            # check if user joined this session

            return Response({"data": data, "date": date_result}, status=200)
        except Exception as e:

            return Response({"error": str(e)}, status=400)

    # user join session
    def post(self, request):
        try:
            session_id = self.request.data["session_id"]
            session = models.Session.objects.get(id=int(session_id))
            session_date = models.SessionDates.objects.get(
                id=int(self.request.data["session_date_id"])
            )
            user = self.request.user
            # ___ join session ___#
            """ this statement check if user didn't finish his all sessions """
            try:
                package = models.Package.objects.get(user=user, sessions=session)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "error": "sorry, Make sure that you  didn't consumed your limit  of this package sessions"
                    },
                    status=400,
                )

            if (
                package.sessions.count()
                <= models.SessionAttendanceRequest.objects.filter(
                    user=user, session__isnull=False, package=package, attended=True
                ).count()
            ):
                "add user to deactivated users of this package"
                today = date.today()
                package_deactivition = package.deactivated_users.add(user)
                package_deactivition = package.user.remove(user)
                payment = accept_models.Payment.objects.get(
                    user=user,
                    Subscription=package,
                    paid=True,
                    end_date__gte=today,
                    deactivated=False,
                )
                payment.deactivated = True
                payment.save()

                return Response(
                    {
                        "error": "sorry you reached your limit quote of sessions please buy another package"
                    },
                    status=400,
                )

            attend = models.SessionAttendanceRequest.objects.create(
                user=user,
                session=session,
                date=session_date,
                package=package,
                joined=True,
            )

            data = serializers.SessionAttendanceSerializer(attend).data
            return Response({"status": "success", "data": data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


"""
User session history 
"""


class MyHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.LoggedInPermission,)

    def get(self, request):
        try:
            user = self.request.user
            old_attended_sessions = models.SessionAttendanceRequest.objects.filter(
                user=user, attended=True
            )
            data = serializers.SessionAttendanceSerializer(
                old_attended_sessions, many=True
            ).data
            return Response({"data": data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


"""
Buy Package View
"""
# time plus one year
def plus3months_time():
    return datetime.now() + timedelta(weeks=13)


class BuyPackageView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.LoggedInPermission,)

    def post(self, request):
        try:
            user = self.request.user
            today = date.today()
            subscription = models.Package.objects.get(
                id=int(self.request.data["package_id"])
            )
            amount = subscription.price
            # Handeling pay in branch senario
            pay_in_branch = self.request.data.get("pay_in_branch", 0)
            # cheack if user already have this plan and he is stupid enough to do this
            try:
                payment = accept_models.Payment.objects.get(
                    user=user,
                    Subscription=subscription,
                    paid=True,
                    end_date__gte=today,
                    deactivated=False,
                )
                return Response({"you already subscribed to this plan"}, status=400)
            except Exception as e:
                pass

            try:
                payment = accept_models.Payment.objects.get(
                    user=user, Subscription=subscription, paid=False, deactivated=False,pay_in_branch=False
                )
                if pay_in_branch == 1:
                    url = None
                else:
                    url = payment.get_iframe_url()

            except ObjectDoesNotExist as e:
                payment = accept_models.Payment.objects.create(
                    title="subscription " + str(subscription.id),
                    user=user,
                    Subscription=subscription,
                    first_name=user.FirstName,
                    last_name=user.SecondName if user.SecondName else "no_last_name",
                    phone=user.mobile if user.mobile else "No Phone Number",
                    email=user.email,
                    currency="EGP",
                    total=amount,
                    date_issued=today,
                    order_id=subscription.id,
                )

                if subscription.period == "3months":
                    payment.end_date = plus3months_time()

                payment.set_payment_key()
                url = payment.get_iframe_url()
                payment.save()
                if pay_in_branch == 1:
                    payment.pay_in_branch = True
                    url = None
                else:
                    payment.pay_in_branch = False
                    url = payment.get_iframe_url()
            # off online payment method for now 27/2/2020
            return Response(
                {"payment_url": url, "pay_in_branch": pay_in_branch}, status=400
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


"""
INFO VIEW 
"""


class GeneralInfoView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.LoggedInPermission,)

    def get(self, request):
        serializer = serializers.InfoSerializer
        faq_serializer = serializers.FAQSerializer
        query = models.GeneralInfo.objects.all()
        FAQ = models.FAQ.objects.all()
        data = serializer(query, many=True).data
        schedule = serializers.ScheduleSerializer(models.Schedule.objects.all(),many=True).data
        faq_data = faq_serializer(FAQ, many=True).data
        
        return Response({"data": data, "FAQ": faq_data,"schedule":schedule})

