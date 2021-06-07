from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.response import Response

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("UserView/", views.UserViews.as_view(), name="user-view"),
    path("UserLogIn/", views.LogInView.as_view(), name="user-log-in"),
    path("PassView/", views.SessionPassView.as_view(), name="user-pass"),
    path(
        "CoachSessionPassView/",
        views.CoachSessionPassView.as_view(),
        name="CoachSessionPassView-pass",
    ),
    path(
        "PackagesCategoryView/",
        views.PackagesCategoryView.as_view(),
        name="PackagesCategoryView",
    ),
    path("MyPackageView/", views.MyPackageView.as_view(), name="MyPackageView"),
    path(
        "UserPlanSessions/", views.UserPlanSessions.as_view(), name="UserPlanSessions"
    ),
    path("MyHistory/", views.MyHistory.as_view(), name="MyHistory"),
    path("BuyPackageView/", views.BuyPackageView.as_view(), name="BuyPackageView"),
    path(
        "SingleSessionDataView/",
        views.SingleSessionDataView.as_view(),
        name="SingleSessionDataView",
    ),
    path("GeneralInfoView/", views.GeneralInfoView.as_view(), name="GeneralInfoView"),
    path("ScheduleSession/", views.ScheduleSession.as_view(), name="ScheduleSession"),
]
