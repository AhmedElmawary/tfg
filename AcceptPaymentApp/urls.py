from django.conf.urls import url, include
from AcceptPaymentApp import views

urlpatterns = [
    url(r"^payments/$", views.PaymentView.as_view()),
    url(r"^payments/iframe/(?P<order_id>[0-9]+)/$", views.IframeUrl.as_view()),
]
