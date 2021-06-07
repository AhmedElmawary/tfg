# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from import_export.admin import ExportActionMixin
from django.contrib import admin
from AcceptPaymentApp import models
from app import models as app_models
from django.contrib import messages

class PaymentAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields = ['first_name','last_name','email']
    
    list_display = (
        "id",
        "title",
        "first_name",
        "last_name",
        "phone",
        "email",
        "currency",
        "total",
        "date_issued",
        "date_of_payment",
        "paid",
        "slug",
        "order_id",
        "payment_key",
        "valu",
        "reason_for_failure",
    )

    def save_model(self, request, obj, form, change):
        if obj.paid == True:    
            package = app_models.Package.objects.get(id=obj.Subscription.id)
            package.user.add(obj.user)
            messages.add_message(request, messages.INFO, 'User Added successfully')
            ## delete all this user attendance requests that deduct from his package in user app pass view 
            deduction = app_models.SessionAttendanceRequest.objects.filter(
                        user=obj.user,
                        package=package,
                        attended=True,
                        joined=True
                        ).delete()

        super(PaymentAdmin, self).save_model(request, obj, form, change)

admin.site.register(models.Payment, PaymentAdmin)
