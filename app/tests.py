from django.test import TestCase
from django.test.client import Client
from app import models 
# Create your tests here.


#create user and login tests
class CreateUserTestCase(TestCase):
    def setUp(self):
        models.User.objects.create(
        FirstName="lion",
        SecondName="kid",
        password="123456",
        email="lionkid@bit68.com",
        gender="Male",
        mobile="01111111111",
        )

    def test_user_login(self):
        """User can login correctly"""
        c = Client()
        c.login(email="lionkid@bit68.com", password="123456")

# create package category test case 
class CreatePackageCategoryTestCase(TestCase):
    def setUp(self):
        models.PackageCategory.objects.create(
            title="test"
        )

# create package  test case 
class CreatePackageTestCase(TestCase):
    def setUp(self):
        u = models.User.objects.first()
        models.Package.objects.create(
            user=u,
            title="test",
            description="test",
            price=1,
            period="Month",
            currency="EGP",
            start_date="2020-11-11",
            end_date="2020-12-11"
        )

    



