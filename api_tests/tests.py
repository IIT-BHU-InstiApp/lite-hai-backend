from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# pylint: disable=unused-wildcard-import, wildcard-import
from .populate_database import *
from .test_utils import *

CLUB_RESPONSE = {
    "id": 1,
    "name": CLUB_NAME,
    "council": {
        "id": 1,
        "name": COUNCIL_NAME,
        "small_image_url": COUNCIL_SMALL_IMAGE_URL,
        "large_image_url": COUNCIL_LARGE_IMAGE_URL
    },
    "small_image_url": CLUB_SMALL_IMAGE_URL,
    "large_image_url": CLUB_LARGE_IMAGE_URL
}

class ApiTests(APITestCase):
    """
    Each endpoint is tested three times

    1. As a secy
    2. As a workshop contact
    3. As a general user
    """
    def setUp(self):
        populate_database()
        # The first value of the tuple should be used as the source of truth
        self.users = [
            ('secy', get_user(SECY_USERNAME)),
            ('contact', get_user(CONTACT_USERNAME)),
            ('general', get_user(GENERAL_USERNAME))
        ]


    def authorize_api_request(self, token):
        """
        Authorize the api request
        """
        # pylint: disable=no-member
        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % token)


    def test_get_profile(self):
        """
        GET /profile/
        """
        url = reverse('profile')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)
            response = self.client.get(url)

            if role == 'secy':
                expected_response_data = {
                    "id": 1,
                    "name": SECY_NAME,
                    "email": SECY_EMAIL,
                    "phone_number": SECY_PHONE,
                    "department": SECY_DEPT,
                    "year_of_joining": SECY_YEAR,
                    "subscriptions": [],
                    "club_privileges": [
                        CLUB_RESPONSE
                    ],
                    "photo_url": SECY_PHOTO
                }

            elif role == 'contact':
                expected_response_data = {
                    "id": 2,
                    "name": CONTACT_NAME,
                    "email": CONTACT_EMAIL,
                    "phone_number": CONTACT_PHONE,
                    "department": CONTACT_DEPT,
                    "year_of_joining": CONTACT_YEAR,
                    "subscriptions": [],
                    "club_privileges": [],
                    "photo_url": CONTACT_PHOTO
                }

            elif role == 'general':
                expected_response_data = {
                    "id": 3,
                    "name": GENERAL_NAME,
                    "email": GENERAL_EMAIL,
                    "phone_number": GENERAL_PHONE,
                    "department": GENERAL_DEPT,
                    "year_of_joining": GENERAL_YEAR,
                    "subscriptions": [
                        CLUB_RESPONSE
                    ],
                    "club_privileges": [],
                    "photo_url": GENERAL_PHOTO
                }

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, expected_response_data)

    def test_put_profile(self):
        """
        PUT /profile/
        """
        url = reverse('profile')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)
            response = self.client.get(url)

            if role == 'secy':
                expected_response_data = {
                    "id": 1,
                    "name": SECY_NAME,
                    "email": SECY_EMAIL,
                    "phone_number": SECY_PHONE,
                    "department": SECY_DEPT,
                    "year_of_joining": SECY_YEAR,
                    "subscriptions": [],
                    "club_privileges": [
                        CLUB_RESPONSE
                    ],
                    "photo_url": SECY_PHOTO
                }

            elif role == 'contact':
                expected_response_data = {
                    "id": 2,
                    "name": CONTACT_NAME,
                    "email": CONTACT_EMAIL,
                    "phone_number": CONTACT_PHONE,
                    "department": CONTACT_DEPT,
                    "year_of_joining": CONTACT_YEAR,
                    "subscriptions": [],
                    "club_privileges": [],
                    "photo_url": CONTACT_PHOTO
                }

            elif role == 'general':
                expected_response_data = {
                    "id": 3,
                    "name": GENERAL_NAME,
                    "email": GENERAL_EMAIL,
                    "phone_number": GENERAL_PHONE,
                    "department": GENERAL_DEPT,
                    "year_of_joining": GENERAL_YEAR,
                    "subscriptions": [
                        CLUB_RESPONSE
                    ],
                    "club_privileges": [],
                    "photo_url": GENERAL_PHOTO
                }

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, expected_response_data)