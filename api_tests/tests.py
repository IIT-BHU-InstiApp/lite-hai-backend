from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
# pylint: disable=unused-wildcard-import, wildcard-import
from .populate_database import *

def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    # pylint: disable=no-member
    token, _ = Token.objects.get_or_create(user=user)
    return token

class ApiTests(APITestCase):
    """
    Each endpoint is tested three times

    1. As a secy
    2. As a workshop contact
    3. As a general user
    """
    def setUp(self):
        populate_database()


    def authorize_api_request(self, token):
        """
        Authorize the api request
        """
        # pylint: disable=no-member
        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % token)


    def test_profile(self):
        """
        Tests the following endpoints

        1. GET /profile/
        2. PUT /profile/
        3. PATCH /profile/
        """
        url = reverse('profile')

