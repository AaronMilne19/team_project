from django.test import TestCase
import requests
from home.models import City
import datetime


# Create your tests here.

# Unit tests -City module tests
class CityTestCase(TestCase):
    def setUp(self):
        City.objects.create(id=0, Name="China", NameSlug='1', Description='good', HeaderPicture='1', Views=0,
                            Added=datetime.datetime.now())

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        city = City.objects.get(Name="China")
        self.assertEqual(city.Name, 'China', 'No Luoyang city found')


# Restful interface testing uses Django's built-in test module.Test login interface
class LoginApiTest(TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/account/login/'

    # Get test login interface is normal
    def test_get_login(self):
        r = requests.get(self.base_url)
        result = r.status_code
        # Whether the end is 200
        self.assertEqual(result, 200, 'Please check the interface status.')

# if __name__ == "__main__":
#     unittest.main()

