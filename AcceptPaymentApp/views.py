# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json

from AcceptPaymentApp import models
from services.helpers import dateNow

# from app import models as Rmodels


class PaymentView(APIView):
    def get(self, request):
        # GET /api/payments/?is_refund=false&id=924994&integration_id=4589&owner=3088&captured_amount=0&is_capture=false&is_voided=false&has_parent_transaction=false&profile_id=2858&is_standalone_payment=true&order=2864049&data.message=Dear+customer%2C+please+download+valU+app+and+apply+to+valU+in+order+to+purchase+online+with+installments.&is_auth=false&created_at=2019-03-11T16%3A58%3A40.952500&pending=false&amount_cents=25000&is_refunded=false&refunded_amount_cents=0&is_void=false&currency=EGP&txn_response_code=103&error_occured=false&is_3d_secure=false&hmac=83c9cf5c11fffa55efdf2b3901520c71f52d1be9a02f28c34621eec98f0c8b5a3e3b6e42f68767f6bc43bfbe3831489d6a09a4eb6d1cefb6249d9b61dd1c9450&source_data.type=valu&merchant_order_id=51c82545-406a-4edc-9c1f-6450bb9a310d&success=false&source_data.sub_type=valu&source_data.pan=%2B201004198275
        success = request.GET["success"]
        if success == "true":
            payment = models.Payment.objects.get(order_id=request.GET["order"])
            payment.paid = True
            order = payment.Subscription
            order.user.add(payment.user)
            ## delete all this user attendance requests that deduct from his package in user app pass view 
            deduction = models.SessionAttendanceRequest.objects.filter(
                        user=payment.user,
                        package=payment.Subscription,
                        attended=True,
                        joined=True
                        ).delete()

            # order.paid = True
            order.save()
            payment.save()
            return Response(
                {"details": "Your Subscription added succesfully"}, status=200
            )

        else:
            return Response(
                {"details": "Failed Transaction please try again"}, status=400
            )

    def post(self, request):
        body_content = request.data
        # paymoblog('POST response', body_content)
        order_id = body_content["obj"]["order"]["id"]
        receipt_url = body_content["obj"]["data"].get("receipt_url", "no receipt url")
        downpayment = body_content["obj"]["data"].get("down_payment", "0")
        success = body_content["obj"]["success"]
        payment = models.Payment.objects.get(order_id=order_id)
        if success:
            payment.paid = True
            payment.date_of_payment = dateNow()
            payment.downpayment = downpayment
            payment.receipt_url_valu = receipt_url
            payment.save()

            order = payment.subscription
            order.user.add(payment.user)
            order.save()
        else:
            """ return products aviliability to its value before order """
            order = payment.Subscription
            payment.failure_response = body_content
            payment.reason_for_failure = body_content["obj"]["data"].get("message", "")
            order = payment.Subscription
            payment.save()
        payment.save()
        return Response()


class IframeUrl(APIView):
    def get(self, request, order_id):

        payment = models.Payment.objects.get(order_id=order_id)
        if payment.paid:
            return Response(
                {"details": ["already paid"]}, status=status.HTTP_400_BAD_REQUEST
            )
        if not payment.payment_key:
            payment.set_payment_key()
        return Response({"iframe_url": payment.get_iframe_url()})
