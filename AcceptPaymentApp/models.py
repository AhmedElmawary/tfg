# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from services.helpers import *
import uuid
import math
from django.core.mail import send_mail
from services.helpers import dateNow, rand_int
import datetime
from tfg.settings import ACCEPT_CONF
from AcceptPaymentApp.paymob_accept import *
from django.utils.crypto import get_random_string


def plus4weeks_time():
    return datetime.datetime.now() + datetime.timedelta(weeks=4)



class Payment(models.Model):
    title = models.CharField(max_length=254)
    user = models.ForeignKey(
        "app.User",
        related_name="package_payment_user",
        null=True,
        on_delete=models.SET_NULL,
    )
    Subscription = models.ForeignKey(
        "app.Package",
        related_name="paymob_payment",
        null=True,
        on_delete=models.SET_NULL,
    )
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254)
    currency = models.CharField(max_length=12, choices=(("EGP", "EGP"), ("$", "$")))
    total = models.FloatField(default=0)
    date_issued = models.DateTimeField(default=dateNow)
    date_of_payment = models.DateTimeField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    slug = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    end_date = models.DateField(default=plus4weeks_time)
    # accept related
    order_id = models.CharField(max_length=100, unique=True, default=get_random_string)
    payment_key = models.TextField(blank=True, null=True)

    reason_for_failure = models.TextField(blank=True, null=True)
    failure_response = models.TextField(blank=True, null=True)
    # valu related
    downpayment = models.TextField(blank=True, null=True)
    valu = models.BooleanField(default=False)
    receipt_url_valu = models.TextField(blank=True, null=True)
    deactivated = models.BooleanField(default=False)
    pay_in_branch = models.BooleanField(default=False)

    def __unicode__(self):
        return "payment ID: " + str(self.id) + ", " + self.title

    def set_payment_key(self):
        get_token_response = get_order_token()
        create_order_response = create_order(
            get_token_response,
            amount=self.actual_amount(),
            currency=self.formated_currency(),
            shipping_info=self.shipping_billing_data(),
            merchant_order_id=str(self.slug),
        )

        card_integration_id = ACCEPT_CONF["EGP_CARDINTEGRATIONID"]
        if self.valu:
            card_integration_id = ACCEPT_CONF["VAUE_CARDINTEGRATIONID"]

        full_dict = generate_payment_key(
            create_order_response,
            card_integration_id,
            self.shipping_billing_data(),
            items=[],
        )

        self.order_id = full_dict["order_id"]
        self.payment_key = full_dict["payment_key"]
        self.save()

    def get_iframe_url(self):
        if self.valu:
            return (
                ACCEPT_CONF["IFRAME_URL"]
                + ACCEPT_CONF["VAUE_IFRAME_ID"]
                + "?payment_token="
                + str(self.payment_key)
            )
        return (
            ACCEPT_CONF["IFRAME_URL"]
            + ACCEPT_CONF["IFRAME_ID"]
            + "?payment_token="
            + str(self.payment_key)
        )

    # helper methods
    def formated_currency(self):
        if self.currency == "$":
            return "USD"
        return "EGP"

    def shipping_billing_data(self):
        data = {
            "apartment": "803",
            "email": self.email,
            "floor": "42",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "street": "Ethan Land",
            "building": "8028",
            "phone_number": self.phone,
            "postal_code": "1231",
            "city": "Jaskolskiburgh",
            "country": "CR",
            "state": "Utah",
        }
        return data

    def actual_amount(self):
        return int(math.ceil(self.total * 100))

    # def get_order_items(self):
    #     order = self.order
    #     order_products = order.orderproduct.all()
    #     return [
    #         {
    #             "name": order_product.product.name,
    #             "description":  order_product.product.sub_category.category.name if order_product.product.sub_category else order_product.product.name,
    #             "amount_cents": int(math.ceil(order_product.product_price * 100 * order_product.quantity)),
    #             "quantity": order_product.quantity
    #         }
    #         for order_product in order_products if order_product.product
    #     ]
