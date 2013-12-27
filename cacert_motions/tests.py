from __future__ import with_statement

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime


from .models import Motion

class MotionTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
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
    
