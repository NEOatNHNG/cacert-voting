from __future__ import with_statement

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime

import django.core.exceptions

from .models import Motion

class MotionTest(TestCase):
    
    CLIENT_CERT = '''
    -----BEGIN CERTIFICATE-----
    MIIBmzCCAVWgAwIBAgIJAJ6nJQDxDeyKMA0GCSqGSIb3DQEBBQUAMDkxFTATBgNV
    BAMMDEFsaWNlIENvb3BlcjEgMB4GCSqGSIb3DQEJARYRYWxpY2VAZXhhbXBsZS5j
    b20wHhcNMTMxMjI3MTkyNzEyWhcNMjUwMzE1MTkyNzEyWjA5MRUwEwYDVQQDDAxB
    bGljZSBDb29wZXIxIDAeBgkqhkiG9w0BCQEWEWFsaWNlQGV4YW1wbGUuY29tMEww
    DQYJKoZIhvcNAQEBBQADOwAwOAIxAOskcOwI4jU07L/wsR1voVoPeWUdSmz6cfH1
    TcLEw0DjKQ9qabImdAZazd7DcoLs8QIDAQABo1AwTjAdBgNVHQ4EFgQU71qcj7il
    AbNhCTYsK8HXnHbX9mgwHwYDVR0jBBgwFoAU71qcj7ilAbNhCTYsK8HXnHbX9mgw
    DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAMxAH5jmSrviBKHmVkPhWtbb1mw
    sfj0L1jexV4nekJLUHx1z7wzwOxGdRhnBAg/7E4EgA==
    -----END CERTIFICATE-----
    '''
    
    @classmethod
    def setUpClass(cls):
        '''
        Create some users
        '''
        super(MotionTest, cls).setUpClass()
        
        cls.alice = User.objects.create_user(
            'alice',
            'alice@example.com',
            'password',
            first_name='Alice',
            last_name='Cooper',
        )
        
        cls.bob = User.objects.create_user(
            'bob',
            'bob@example.com',
            'password',
            first_name='Bob',
            last_name='Dylan',
        )
        
        cls.carole = User.objects.create_user(
            'carole',
            'carole@example.com',
            'password',
            first_name='Carol',
            last_name='King',
        )
        
        cls.dave = User.objects.create_user(
            'dave',
            'dave@example.com',
            'password',
            first_name='Dave',
            last_name='Brubek',
        )
        
        cls.erin = User.objects.create_user(
            'erin',
            'erin@example.com',
            'password',
            first_name='Erin',
            last_name='Anttila',
        )
        
        cls.frank = User.objects.create_user(
            'frank',
            'frank@example.com',
            'password',
            first_name='Frank',
            last_name='Sinatra',
        )
        
        cls.gloria = User.objects.create_user(
            'gloria',
            'gloria@example.com',
            'password',
            first_name='Gloria',
            last_name='Gaynor',
        )
    
    def create_motion(self,
                      title='Test motion',
                      text='Text of the test motion',
                      proponent=None,
                      due=timezone.now() + timedelta(days=3),
                      **kwargs
                      ):
        '''
        Helper for easy creation of test motions
        '''
        if not proponent:
            proponent=self.alice
        
        m = Motion(
            title=title,
            text=text,
            proponent=proponent,
            due=due,
            **kwargs
        )
        m.save()
        return m
    
    def test_create_motion(self):
        '''
        Test if the motion creation works properly including generating
        motion numbers
        '''
        m = self.create_motion()
        
        # Make sure that motion index starts with 1
        with self.assertRaises(Motion.DoesNotExist,
                               msg='There is a motion starting with index "0"'):
            Motion.objects.get(
                number=u'm{now.year}{now.month}{now.day}.0'.format(now=datetime.utcnow()),
            )
        
        self.assertIsInstance(
            Motion.objects.get(
                number=u'm{now.year}{now.month}{now.day}.1'.format(now=datetime.utcnow()),
            ),
            Motion,
            'Motion with index "1" seems to be missing',
        )
        self.assertEqual(
            m,
            Motion.objects.get(pk=m.pk),
            'Freshly added motion not present in database',
        )
        
        # Make sure a new motion gets a different number
        m2 = self.create_motion(title='Second test motion')
        self.assertNotEqual(
            m.number,
            m2.number,
            'Duplicate motion number'
        )
    
    def test_vote(self):
        '''
        Test if votes are properly counted
        '''
        m = self.create_motion()
        
        # precondition
        self.assertEqual(0, m.ayes().count())
        self.assertEqual(0, m.nays().count())
        self.assertEqual(0, m.abstains().count())
        
        m.vote(True, self.alice, self.CLIENT_CERT)
        self.assertEqual(1, m.ayes().count())
        self.assertEqual(0, m.nays().count())
        self.assertEqual(0, m.abstains().count())
        
        m.vote(False, self.bob, self.CLIENT_CERT)
        self.assertEqual(1, m.ayes().count())
        self.assertEqual(1, m.nays().count())
        self.assertEqual(0, m.abstains().count())
        
        m.vote(None, self.carole, self.CLIENT_CERT)
        self.assertEqual(1, m.ayes().count())
        self.assertEqual(1, m.nays().count())
        self.assertEqual(1, m.abstains().count())
        
        m.proxy_vote(vote=True,
                     voter=self.dave,
                     proxy=self.alice,
                     justification='Vote during board meeting',
                     certificate=self.CLIENT_CERT)
        self.assertEqual(2, m.ayes().count())
        self.assertEqual(1, m.nays().count())
        self.assertEqual(1, m.abstains().count())
        
        m.proxy_vote(vote=False,
                     voter=self.erin,
                     proxy=self.alice,
                     justification='Vote during board meeting',
                     certificate=self.CLIENT_CERT)
        self.assertEqual(2, m.ayes().count())
        self.assertEqual(2, m.nays().count())
        self.assertEqual(1, m.abstains().count())
        
        m.proxy_vote(vote=True,
                     voter=self.frank,
                     proxy=self.bob,
                     justification='Vote during board meeting',
                     certificate=self.CLIENT_CERT)
        self.assertEqual(3, m.ayes().count())
        self.assertEqual(2, m.nays().count())
        self.assertEqual(1, m.abstains().count())
        
        m.proxy_vote(vote=None,
                     voter=self.gloria,
                     proxy=self.alice,
                     justification='Vote during board meeting',
                     certificate=self.CLIENT_CERT)
        self.assertEqual(3, m.ayes().count())
        self.assertEqual(2, m.nays().count())
        self.assertEqual(2, m.abstains().count())
    
    def test_duplicate_vote(self):
        '''
        Test if creating duplicate votes is blocked
        '''
        m = self.create_motion()
        m.vote(True, self.alice, self.CLIENT_CERT)
        
        with self.assertRaises(django.core.exceptions.ValidationError,
                               msg='Duplicate vote detected'):
            m.vote(False, self.alice, self.CLIENT_CERT)
        
        with self.assertRaises(django.core.exceptions.ValidationError,
                               msg='Duplicate proxy vote detected'):
            m.proxy_vote(vote=False,
                         voter=self.alice,
                         proxy=self.bob,
                         justification='Vote during board meeting',
                         certificate=self.CLIENT_CERT)
    
    
    def test_self_proxy(self):
        '''
        Test if creating proxy votes for oneself is blocked
        '''
        m = self.create_motion()
        with self.assertRaises(django.core.exceptions.ValidationError,
                               msg='Self-proxy detected'):
            m.proxy_vote(vote=True,
                         voter=self.alice,
                         proxy=self.alice,
                         justification='Vote during board meeting',
                         certificate=self.CLIENT_CERT)
