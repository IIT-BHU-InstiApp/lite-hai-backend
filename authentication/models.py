from django.db import models
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    uid = models.CharField(max_length=64)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=60)
    year_of_joining = models.CharField(max_length=10)
    photo_url = models.URLField(null=True, blank=True, editable=False)
    can_post_notice = models.BooleanField(default=False)

    # pylint: disable=invalid-str-returned
    def __str__(self):
        return self.name

    def get_council_privileges(self):
        """
        Get the privileges of the user for managing Council details
        Councils - General Secretary / Joint General Secretary
        """
        # pylint: disable=no-member
        councils = self.council_gensec.all()
        councils = councils.union(self.council_joint_gensec.all())
        return councils

    def get_club_privileges(self):
        """
        Get the privileges of the user for creating workshops
        Clubs - Secretary / Joint Secretary,
        Councils - General Secretary / Joint General Secretary
        """
        # pylint: disable=no-member
        clubs = self.club_secy.all().select_related('council')
        clubs = clubs.union(self.club_joint_secy.all().select_related('council'))
        council_gensec = self.council_gensec
        council_joint_gensec = self.council_joint_gensec
        for council in council_gensec.all():
            clubs = clubs.union(council.clubs.all().select_related('council'))
        for council in council_joint_gensec.all():
            clubs = clubs.union(council.clubs.all().select_related('council'))
        return clubs

    def get_workshop_privileges(self):
        """
        Get the privileges of the user for modifying workshops
        """
        # pylint: disable=no-member
        workshops = self.organized_workshops.all()
        return workshops

    def get_entity_privileges(self):
        """
        Get the privileges of the user for creating events
        Entities - Point of Contact,
        """
        # pylint: disable=no-member
        entities = self.entity_point_of_contact.all()
        return entities
