from django.test import TestCase, Client, SimpleTestCase
from home.models import *
from home.views import *
from Account.views import *
from Account.models import *
from django.db import IntegrityError
import datetime
from django.urls import reverse, resolve

from team_project.settings import STATIC_DIR
import json
import datetime

from django.contrib import auth  

from django.contrib.auth.models import User as AuthUser  


class TestUrls(SimpleTestCase):

    def test_sign_up_url_is_resolved(self):
        url = reverse('Account:sign-up')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('Account:login')
        self.assertEqual(resolve(url).func, login)

    def test_account_url_is_resolved(self):
        url = reverse('Account:account')
        self.assertEqual(resolve(url).func, account)

    def test_setting_url_is_resolved(self):
        url = reverse('Account:setting')
        self.assertEqual(resolve(url).func, upload_avatar)

    def test_loginout_url_is_resolved(self):
        url = reverse('Account:loginout')
        self.assertEqual(resolve(url).func, loginout)


class TestAccountViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.sign_up_url = reverse('Account:sign-up')
        self.login_url = reverse('Account:login')
        self.account_url = reverse('Account:account')
        self.setting_url = reverse('Account:setting')
        self.logout_url = reverse('Account:loginout')

    def test_a_sign_up(self, is_main=None):
        if not is_main:
            return
        response = self.client.get(self.sign_up_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        data = {'username': 'test',
                'surname': 1,
                'fristname': 1,
                'brith': '2021-04-04',
                'email': 'test@qq.com',
                'password': 123,
                'confirmpassword': 123}

        response = self.client.post(self.sign_up_url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(self.client.cookies.keys()), ['sessionid'])


    def test_b_login(self,is_main=None):
        if not is_main:
            return
        data = {'username': 'test',
                'password': 123, }

        response = self.client.post(self.login_url, data=data)

        self.assertEquals(response.status_code, 200)

    def test_c_upload_avatar(self,is_main=None):
        if not is_main:
            return
        file_name = os.path.join(STATIC_DIR, 'images\\test.jpg')
        with open(file_name, 'rb') as fp:
            response = self.client.post(self.setting_url, {'file': fp})

            self.assertEquals(response.status_code, 200)

    def test_d_loginout(self,is_main=None):
        if not is_main:
            return
        # Logout returns 302 redirection
        # The sessionID in the cookie is cleared
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)

    def test_main(self):
        # Because of the randomness of Django test's execution, main is used to ensure the order of execution,
        # and arguments are added to avoid being called by a function other than main
        is_main = True
        self.test_a_sign_up(is_main)
        self.test_b_login(is_main)
        self.test_c_upload_avatar(is_main)
        self.test_d_loginout(is_main)
