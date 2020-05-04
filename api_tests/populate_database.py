from datetime import datetime
from authentication.models import UserProfile, User
from team.models import Role, TeamMember
from workshop.models import Council, Club, Tag, Workshop

# Secy
SECY_USERNAME = 'secy_username'
SECY_EMAIL = 'secy.cse18@itbhu.ac.in'
SECY_UID = 'secy_uid'
SECY_NAME = 'Secy Name'
SECY_PHONE = '1234567890'
SECY_DEPT = 'CSE'
SECY_YEAR = '2020'
SECY_PHOTO = 'https://secy.com/'

# Workshop Contact
CONTACT_USERNAME = 'contact_username'
CONTACT_EMAIL = 'contact.cse18@itbhu.ac.in'
CONTACT_UID = 'contact_uid'
CONTACT_NAME = 'Contact Name'
CONTACT_PHONE = '1234567890'
CONTACT_DEPT = 'CSE'
CONTACT_YEAR = '2020'
CONTACT_PHOTO = 'https://contact.com/'

# General User
GENERAL_USERNAME = 'general_username'
GENERAL_EMAIL = 'general.cse18@itbhu.ac.in'
GENERAL_UID = 'general_uid'
GENERAL_NAME = 'General Name'
GENERAL_PHONE = '1234567890'
GENERAL_DEPT = 'CSE'
GENERAL_YEAR = '2020'
GENERAL_PHOTO = 'https://general.com/'

# Council
COUNCIL_NAME = 'council_name'
COUNCIL_DESCRIPTION = 'council_description'
# Secy, Joint Secy both will be secy
COUNCIL_SMALL_IMAGE_URL = 'https://council-small_image.com/'
COUNCIL_LARGE_IMAGE_URL = 'https://council-large_image.com/'
COUNCIL_WEBSITE_URL = 'https://council-website.com/'
COUNCIL_FACEBOOK_URL = 'https://council-facebook.com/'
COUNCIL_TWITTER_URL = 'https://council-twitter.com/'
COUNCIL_INSTAGRAM_URL = 'https://council-instagram.com/'
COUNCIL_LINKEDIN_URL = 'https://council-linkedin.com/'
COUNCIL_YOUTUBE_URL = 'https://council-youtube.com/'

# Club
CLUB_NAME = 'club_name'
CLUB_DESCRIPTION = 'club_description'
# Secy, Joint Secy both will be secy
CLUB_SMALL_IMAGE_URL = 'https://club-small_image.com/'
CLUB_LARGE_IMAGE_URL = 'https://club-large_image.com/'
CLUB_WEBSITE_URL = 'https://club-website.com/'
CLUB_FACEBOOK_URL = 'https://club-facebook.com/'
CLUB_TWITTER_URL = 'https://club-twitter.com/'
CLUB_INSTAGRAM_URL = 'https://club-instagram.com/'
CLUB_LINKEDIN_URL = 'https://club-linkedin.com/'
CLUB_YOUTUBE_URL = 'https://club-youtube.com/'

# Tag
TAG_NAME = 'tag-name'

# Role
ROLE = 'developer'

# Team Member
TEAM_MEMBER_NAME = 'team_member_name'
GITHUB_USERNAME = 'nishantwrp'

# Workshop
WORKSHOP_TITLE = 'workshop_title'
WORKSHOP_DESCRIPTION = 'workshop_description'
# Date and time can be defaulted to now
WORKSHOP_LOCATION = 'workshop_location'
WORKSHOP_LATITUDE = 14
WORKSHOP_LONGITUDE = 3
WORKSHOP_AUDIENCE = 'everyone'
WORKSHOP_RESOURCES = 'workshop_resources'
# Contact will be contact
# Secy will be intrested user
WORKSHOP_IMAGE = 'https://workshop-image.com/'
# Tag will be tag

def populate_database():
    """
    Create dummy values in the database
    """

    # Create Users
    secy_user = User.objects.create_user(username=SECY_USERNAME, email=SECY_EMAIL)
    contact_user = User.objects.create_user(username=CONTACT_USERNAME, email=CONTACT_EMAIL)
    general_user = User.objects.create_user(username=GENERAL_USERNAME, email=GENERAL_EMAIL)

    # Create UserProfiles
    # pylint: disable=no-member
    secy_userprofile = UserProfile.objects.create(
        uid=SECY_UID, user=secy_user, name=SECY_NAME, email=SECY_EMAIL, phone_number=SECY_PHONE,
        department=SECY_DEPT, year_of_joining=SECY_YEAR, photo_url=SECY_PHOTO)
    contact_userprofile = UserProfile.objects.create(
        uid=CONTACT_UID, user=contact_user, name=CONTACT_NAME, email=CONTACT_EMAIL,
        phone_number=CONTACT_PHONE, department=CONTACT_DEPT, year_of_joining=CONTACT_YEAR,
        photo_url=CONTACT_PHOTO)
    genereal_userprofile = UserProfile.objects.create(
        uid=GENERAL_UID, user=general_user, name=GENERAL_NAME, email=GENERAL_EMAIL,
        phone_number=GENERAL_PHONE, department=GENERAL_DEPT, year_of_joining=GENERAL_YEAR,
        photo_url=GENERAL_PHOTO)

    # Create Council
    council = Council.objects.create(
        name=COUNCIL_NAME, description=COUNCIL_DESCRIPTION, gensec=secy_userprofile,
        small_image_url=COUNCIL_SMALL_IMAGE_URL, large_image_url=COUNCIL_LARGE_IMAGE_URL,
        website_url=COUNCIL_WEBSITE_URL, facebook_url=COUNCIL_FACEBOOK_URL,
        twitter_url=COUNCIL_TWITTER_URL, instagram_url=COUNCIL_INSTAGRAM_URL,
        linkedin_url=COUNCIL_LINKEDIN_URL, youtube_url=COUNCIL_YOUTUBE_URL
    )
    council.joint_gensec.add(secy_userprofile)
    council.save()

    # Create Club
    club = Club.objects.create(
        name=CLUB_NAME, description=CLUB_DESCRIPTION, secy=secy_userprofile,
        small_image_url=CLUB_SMALL_IMAGE_URL, large_image_url=CLUB_LARGE_IMAGE_URL,
        website_url=CLUB_WEBSITE_URL, facebook_url=CLUB_FACEBOOK_URL,
        twitter_url=CLUB_TWITTER_URL, instagram_url=CLUB_INSTAGRAM_URL,
        linkedin_url=CLUB_LINKEDIN_URL, youtube_url=CLUB_YOUTUBE_URL,
        council=council
    )
    club.joint_secy.add(secy_userprofile)
    club.subscribed_users.add(genereal_userprofile)
    club.save()

    # Create tag
    tag = Tag.objects.create(
        tag_name=TAG_NAME, club=club
    )

    # Create role
    role = Role.objects.create(
        role=ROLE
    )

    # Create team member
    TeamMember.objects.create(
        name=TEAM_MEMBER_NAME, role=role,
        github_username=GITHUB_USERNAME
    )

    # Create workshop
    workshop = Workshop.objects.create(
        title=WORKSHOP_TITLE, description=WORKSHOP_DESCRIPTION, club=club,
        date=datetime.now(), time=datetime.now(), location=WORKSHOP_LOCATION,
        audience=WORKSHOP_AUDIENCE, resources=WORKSHOP_RESOURCES, image_url=WORKSHOP_IMAGE
    )
    workshop.contacts.add(contact_userprofile)
    workshop.interested_users.add(secy_userprofile)
    workshop.tags.add(tag)
    workshop.save()
