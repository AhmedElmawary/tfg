from app import models as app_models
from AcceptPaymentApp import models as accept_models

# lst = []
# codes = open('qr_codes.txt','r').readlines()
pk = app_models.Package.objects.get(title="test")
# for code in codes :
#     code=code.replace('\n','')
#     user = app_models.User.objects.create(
#         FirstName=code+"_Dummy",
#         SecondName=code+"_second name",
#         email=code+"@example.com",
#         key=code
#     )
#     pk.user.add(user)
#     pk.save()
#     payment = accept_models.Payment.objects.create(
#         title="Test",
#         user=user,
#         first_name=user.FirstName,
#         last_name=user.SecondName,
#         email=user.email,
#         currency="EGP",
#         total=1,
#         paid=True
#     )
for p in accept_models.Payment.objects.exclude(Subscription=pk):
    p.Subscription = pk
    p.save()


print("finished")
