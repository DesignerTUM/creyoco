"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class BasicTest(TestCase):
    TEST_USER = 'user'
    TEST_PASSWORD = 'password'
    CONTENT = "test test test"
    FILE_NAME = "test.txt"

    def setUp(self):
        user = User.objects.create_user(username=self.TEST_USER,
                                        password=self.TEST_PASSWORD)
        media_path = user.profile.media_path
        open(os.path.join(media_path, self.FILE_NAME), 'w').write(self.CONTENT)
        self.file_url = user.profile.media_url + self.FILE_NAME
        self.client = Client()

    def test_basic_access(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.client.login(username=self.TEST_USER,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.file_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.CONTENT)

    def test_403_on_illegal(self):
        wrong_name = 'user2'
        wrong_password = 'password2'
        wrong_user = User.objects.create_user(username=wrong_name,
                                              password=wrong_password)
        self.client.login(username=wrong_name, password=wrong_password)
        response = self.client.get(self.file_url)
        self.assertEqual(response.status_code, 403)

    def test_superuser(self):
        superlogin = 'admin'
        superpass = 'secret'
        superuser = User.objects.create_superuser(superlogin,
                                                  "super@creyoco.com",
                                                  superpass)

        self.client.login(username=superlogin, password=superpass)
        response = self.client.get(self.file_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.CONTENT)
