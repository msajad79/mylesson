from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, get_user

from .models import Profile, University, FieldStudy

class SignUpTest(TestCase):
    def setUp(self) -> None:
        #User.objects.create_user(username='user1',email='ex@ex.com',password='1234')
        University.objects.create(id=1, name='u1')
        FieldStudy.objects.create(id=1, name='fs1')

    def test_signup_form(self):
        data = {
            'username': 'user1',
            'email': 'ex@ex.com',
            'password1': 'th1s 1s s00000 hard pa55word',
            'password2': 'th1s 1s s00000 hard pa55word',
            'university': 1,
            'fieldstudy' : 1
        }
        res_register = self.client.post('/accounts/signup/', data=data)
        
        self.assertEqual(res_register.status_code, 200)

        self.assertTrue(User.objects.filter(username='user1').exists())
        user1 = User.objects.get(username='user1')
        res_login = self.client.login(username=data['username'], password=data['password1'])
        self.assertFalse(res_login)
        self.assertFalse(user1.is_active)

        self.assertEqual(user1.profile.university.name, 'u1')
        

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0], 'Email Confirm')
        body = mail.outbox[0].body
        soup = BeautifulSoup(body, 'html.parser')
        link_activate = soup.find('a', id='activate_link')
        self.assertNotEqual(link_activate, None)
        link_activate = link_activate['href']

        res_activate = self.client.get(link_activate)

        self.assertEqual(res_activate.status_code, 200)

        self.assertTrue(User.objects.get(username='user1').is_active)

        res_login = self.client.login(username=data['username'], password=data['password1'])
        self.assertTrue(res_login)


class LoginTest(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(username='user1',email='ex@ex.com',password='1234')
        us1 = University.objects.create(id=1, name='u1')
        fs1 = FieldStudy.objects.create(id=1, name='fs1')
        user1.profile.university = us1
        user1.profile.fieldstudy = fs1
        user1.save()


    def test_login_form(self):
        data = {
            'username': 'user1',
            'password': '1234' 
        }
        res_login = self.client.post('/accounts/login/', data=data)
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)


class ResetPasswordTest(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(username='user1',email='ex@ex.com',password='1234')
        us1 = University.objects.create(id=1, name='u1')
        fs1 = FieldStudy.objects.create(id=1, name='fs1')
        user1.profile.university = us1
        user1.profile.fieldstudy = fs1
        user1.save()


    def test_all_form(self):
        data = {
            'email': 'ex@ex.com'
        }
        res_reset = self.client.post('/accounts/password_reset/', data=data)
        self.assertEqual(res_reset.status_code, 302)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0], 'Password Reset Requested')
        body = mail.outbox[0].body
        soup = BeautifulSoup(body, 'html.parser')
        link_activate = soup.find('a', id='password_reset_link')
        self.assertNotEqual(link_activate, None)
        link_reset_password = link_activate['href']

        res_reset = self.client.get(link_reset_password, follow=True)
        self.assertEqual(res_reset.status_code, 200)

        link_reset_password = res_reset.redirect_chain[0][0]

        data = {
            'new_password1':'Th15 5oO 53Cr3T',
            'new_password2':'Th15 5oO 53Cr3T'
        }
        res_reset = self.client.post(link_reset_password, data=data, follow=True)

        res_login = self.client.login(username='user1', password='Th15 5oO 53Cr3T')
        self.assertTrue(res_login)

