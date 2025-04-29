
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from ..models import UserProfile
from ..serializers import User 
from ..middleware import ClassMiddleware
from ..hashing.lsh_strategy import LSHStrategy 
from ..encryption.ckks_strategy import CKKSStrategy

class ClassMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ClassMiddleware(get_response=lambda request: None)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        UserProfile.objects.create(user=self.user, hashing_type='LSH', encryption_type='CKKS')


    def test_authenticated_user(self):
        # Simulate an authenticated user
        print ("middle ware test authenticated " )
        hm = self.client.login(username='testuser', password='testpass')
        request = self.factory.get('/')
        request.user = self.user
        # Call the middleware
        response = self.middleware(request)
        # Check if instances are created
        self.assertIsNotNone(request.CkksInstance)
        self.assertIsInstance(request.CkksInstance, CKKSStrategy)
        self.assertIsNotNone(request.LshInstance)
        self.assertIsInstance(request.LshInstance, LSHStrategy )

    def test_unauthenticated_user(self):
        # Simulate an unauthenticated user
        print ("middle ware test unauthenticated " )
        request = self.factory.get('/')
        request.user = AnonymousUser()   # An anonymous user 
        # Call the middleware
        response = self.middleware(request)
        # Check if instances are None
        self.assertIsNone(request.CkksInstance)
        self.assertIsNone(request.LshInstance)