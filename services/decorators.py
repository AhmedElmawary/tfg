from datetime import datetime, timedelta, date

from django.core.exceptions import ObjectDoesNotExist

from app4R import models
from tpay.models import TpayPayment
from AcceptPaymentApp.models import Payment as AcceptPayment

from services.exceptions import HttpError


def get_subscribtion(function):
    def check_paid(subscription):
        payment_classes = [
            AcceptPayment,
        ]
        for payment_class in payment_classes:
            try:
                payment = payment_class.objects.get(Subscription=subscription)
                if payment.paid:
                    raise HttpError(
                        {
                            "error": "already subscription paid till %s"
                            % (subscription.date_to)
                        },
                        status=400,
                    )
            except ObjectDoesNotExist as e:
                pass

    def wrapper(self, request):
        today = datetime.today()
        date_to = datetime.today() + timedelta(days=30)
        user = request.user

        subscriptions = models.Subscription.objects.filter(
            user=user, date_from__lte=today, date_to__gte=today
        )
        if subscriptions:
            subscription = subscriptions[0]
        else:
            subscription = models.Subscription.objects.create(
                user=user, date_from=today, date_to=date_to,
            )
        check_paid(subscription)
        request.subscription = subscription
        return function(self, request)

    return wrapper
