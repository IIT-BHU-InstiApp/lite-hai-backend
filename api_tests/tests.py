
"""
Endpoints with tests

1. GET /profile/
2. POST /profile/search/
3. GET /team/
4. GET /tags/search/
5. GET /councils/
6. POST /tags/create/
7.

Endpoints with no tests

1. PUT /profile/ (Due to firebase)
2. PATCH /profile/ (Due to firebase)
3. POST /login/ (Due to firebase)
"""
from django.urls import reverse
from rest_framework.test import APITestCase
# pylint: disable=unused-wildcard-import, wildcard-import
from .populate_database import *
from .test_utils import *

NOT_AUTHORIZED_RESPONSE = {
    "detail": "You are not authorized to perform this task"
}

TEAM_MEMBER_RESPONSE = {
    "role": ROLE,
    "team_members": [
        {
            "name": TEAM_MEMBER_NAME,
            "github_username": GITHUB_USERNAME,
            "github_image_url": "https://avatars3.githubusercontent.com/u/36989112?v=4"
        }
    ]
}

COUNCIL_RESPONSE = {
    "id": 1,
    "name": COUNCIL_NAME,
    "small_image_url": COUNCIL_SMALL_IMAGE_URL,
    "large_image_url": COUNCIL_LARGE_IMAGE_URL
}

CLUB_RESPONSE = {
    "id": 1,
    "name": CLUB_NAME,
    "council": COUNCIL_RESPONSE,
    "small_image_url": CLUB_SMALL_IMAGE_URL,
    "large_image_url": CLUB_LARGE_IMAGE_URL
}

SECY_PROFILE_RESPONSE = {
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

SECY_SHORT_PROFILE_RESPONSE = {
    "id": 1,
    "name": SECY_NAME,
    "email": SECY_EMAIL,
    "phone_number": SECY_PHONE,
    "photo_url": SECY_PHOTO
}

CONTACT_PROFILE_RESPONSE = {
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

CONTACT_SHORT_PROFILE_RESPONSE = {
    "id": 1,
    "name": CONTACT_NAME,
    "email": CONTACT_EMAIL,
    "phone_number": CONTACT_PHONE,
    "photo_url": CONTACT_PHOTO
}

GENERAL_PROFILE_RESPONSE = {
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

GENERAL_SHORT_PROFILE_RESPONSE = {
    "id": 1,
    "name": GENERAL_NAME,
    "email": GENERAL_EMAIL,
    "phone_number": GENERAL_PHONE,
    "photo_url": GENERAL_PHOTO
}

TAG_RESPONSE = {
    "id": 1,
    "tag_name": TAG_NAME,
    "club": CLUB_RESPONSE
}


COUNCIL_DETAIL_RESPONSE = {
    "id": 1,
    "name": COUNCIL_NAME,
    "description": COUNCIL_DESCRIPTION,
    "gensec": SECY_SHORT_PROFILE_RESPONSE,
    "joint_gensec": [
        SECY_SHORT_PROFILE_RESPONSE
    ],
    "clubs": [
        CLUB_RESPONSE
    ],
    "small_image_url": COUNCIL_SMALL_IMAGE_URL,
    "large_image_url": COUNCIL_LARGE_IMAGE_URL,
    "website_url": COUNCIL_WEBSITE_URL,
    "facebook_url": COUNCIL_FACEBOOK_URL,
    "twitter_url": COUNCIL_TWITTER_URL,
    "instagram_url": COUNCIL_INSTAGRAM_URL,
    "linkedin_url": COUNCIL_LINKEDIN_URL,
    "youtube_url": COUNCIL_YOUTUBE_URL
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
                expected_response_data = SECY_PROFILE_RESPONSE

            elif role == 'contact':
                expected_response_data = CONTACT_PROFILE_RESPONSE

            elif role == 'general':
                expected_response_data = GENERAL_PROFILE_RESPONSE

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_response_data)

    def test_post_profile_search(self):
        """
        POST /profile/search/
        """
        url = reverse('profile-search')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)

            data = {
                'search_by': 'name',
                'search_string': GENERAL_NAME
            }
            response = self.client.post(url, data=data)

            if role == 'secy':
                expected_response_data = [
                    GENERAL_PROFILE_RESPONSE
                ]
                expected_response_status_code = 200

            elif role == 'contact':
                expected_response_data = NOT_AUTHORIZED_RESPONSE
                expected_response_status_code = 403

            elif role == 'general':
                expected_response_data = NOT_AUTHORIZED_RESPONSE
                expected_response_status_code = 403

            self.assertEqual(response.status_code, expected_response_status_code)
            self.assertEqual(response.json(), expected_response_data)

    def test_get_team(self):
        """
        GET /team/
        """
        url = reverse('team')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)

            response = self.client.get(url)

            if role == 'secy':
                expected_response_data = [
                    TEAM_MEMBER_RESPONSE
                ]
                expected_response_status_code = 200

            elif role == 'contact':
                expected_response_data = [
                    TEAM_MEMBER_RESPONSE
                ]
                expected_response_status_code = 200

            elif role == 'general':
                expected_response_data = [
                    TEAM_MEMBER_RESPONSE
                ]
                expected_response_status_code = 200

            self.assertEqual(response.status_code, expected_response_status_code)
            self.assertEqual(response.json(), expected_response_data)

    def test_post_tag_create(self):
        """
        POST /tags/create/
        """
        url = reverse('tag-create')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)

            NEW_TAG_NAME = 'second-tag'

            data = {
                'tag_name': NEW_TAG_NAME,
                'club': 1
            }

            response = self.client.post(url, data=data)
            tag_response = TAG_RESPONSE
            if response.status_code == 200:
                tag_response['id'] = Tag.objects.get(tag_name=NEW_TAG_NAME).id
            tag_response['tag_name'] = NEW_TAG_NAME

            # Cleanup database
            Tag.objects.filter(tag_name=NEW_TAG_NAME).delete()

            if role == 'secy':
                expected_response_data = tag_response
                expected_response_status_code = 200

            elif role == 'contact':
                # TODO: Fix this
                expected_response_data = {
                    'non_field_errors': ['You are not allowed to create tag for this club']
                }
                expected_response_status_code = 400

            elif role == 'general':
                expected_response_data = NOT_AUTHORIZED_RESPONSE
                expected_response_status_code = 403

            self.assertEqual(response.status_code, expected_response_status_code)
            self.assertEqual(response.json(), expected_response_data)

            # Reset the value of TAG_RESPONSE
            TAG_RESPONSE['tag_name'] = TAG_NAME
            TAG_RESPONSE['id'] = 1

    def test_post_tag_search(self):
        """
        POST /tags/search/
        """
        url = reverse('tag-search')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)

            data = {
                'tag_name': TAG_NAME,
                'club': 1
            }

            response = self.client.post(url, data=data)

            if role == 'secy':
                expected_response_data = [TAG_RESPONSE]
                expected_response_status_code = 200

            elif role == 'contact':
                expected_response_data = [TAG_RESPONSE]
                expected_response_status_code = 200

            elif role == 'general':
                expected_response_data = [TAG_RESPONSE]
                expected_response_status_code = 200

            self.assertEqual(response.status_code, expected_response_status_code)
            self.assertEqual(response.json(), expected_response_data)

    def test_get_councils(self):
        """
        GET /councils/
        """
        url = reverse('councils')

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)

            response = self.client.get(url)

            if role == 'secy':
                expected_response_data = [COUNCIL_RESPONSE]
                expected_response_status_code = 200

            elif role == 'contact':
                expected_response_data = [COUNCIL_RESPONSE]
                expected_response_status_code = 200

            elif role == 'general':
                expected_response_data = [COUNCIL_RESPONSE]
                expected_response_status_code = 200

            self.assertEqual(response.status_code, expected_response_status_code)
            self.assertEqual(response.json(), expected_response_data)

    def test_get_council_detail(self):
        """
        GET /councils/{id}/
        """
        url = reverse('council-detail', kwargs={'pk': 1})

        for role, user in self.users:
            self.authorize_api_request(user.auth_token)

            response = self.client.get(url)

            if role == 'secy':
                expected_response_data = COUNCIL_DETAIL_RESPONSE
                expected_response_status_code = 200

            elif role == 'contact':
                expected_response_data = COUNCIL_DETAIL_RESPONSE
                expected_response_status_code = 200

            elif role == 'general':
                expected_response_data = COUNCIL_DETAIL_RESPONSE
                expected_response_status_code = 200

            self.assertEqual(response.status_code, expected_response_status_code)
            self.assertEqual(response.json(), expected_response_data)

    # def test_put_council_detail(self):
    #     """
    #     PUT /councils/{id}/
    #     """
    #     url = reverse('council-detail', kwargs={'pk': 1})

    #     for role, user in self.users:
    #         self.authorize_api_request(user.auth_token)

    #         response = self.client.put(url)

    #         if role == 'secy':
    #             expected_response_data = COUNCIL_DETAIL_RESPONSE
    #             expected_response_status_code = 200

    #         elif role == 'contact':
    #             # TODO: Fix this
    #             expected_response_data = COUNCIL_DETAIL_RESPONSE
    #             expected_response_status_code = 200

    #         elif role == 'general':
    #             # TODO: Fix this
    #             expected_response_data = COUNCIL_DETAIL_RESPONSE
    #             expected_response_status_code = 200

    #         self.assertEqual(response.status_code, expected_response_status_code)
    #         self.assertEqual(response.json(), expected_response_data)