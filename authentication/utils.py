import logging
from firebase_admin import auth, messaging, exceptions
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.exceptions import ValidationError
from google.auth.exceptions import TransportError

logger = logging.getLogger('django')

class Student:

    dept_list = {
        'bce': 'Biochemical Engineering',
        'bme': 'Biomedical Engineering',
        'cer': 'Ceramic Engineering',
        'che': 'Chemical Engineering',
        'chy': 'Chemistry',
        'civ': 'Civil Engineering',
        'cse': 'Computer Science and Engineering',
        'ece': 'Electronics Engineering',
        'eee': 'Electrical Engineering',
        'mat': 'Mathematics and Computing',
        'mec': 'Mechanical Engineering',
        'met': 'Metallurgical Engineering',
        'min': 'Mining Engineering',
        'mst': 'Materials Science and Technology',
        'phe': 'Pharmaceutical Engineering and Technology',
        'phy': 'Physics',
        'hss': 'Humanistic Studies'
    }

    @classmethod
    def get_department_code(cls, email):
        """
        Get department code from email id
        """
        username = email.split('@')[0]
        dept_code = username.split('.')[-1][:3]
        return dept_code

    @classmethod
    def get_department(cls, email):
        """
        Get department name from email id
        """
        dept_code = cls.get_department_code(email)
        return cls.dept_list[dept_code]

    @classmethod
    def get_year(cls, email):
        """
        Get year from email id
        """
        username = email.split('@')[0]
        year = username.split('.')[-1][3:]
        return '20' + year

    @classmethod
    def verify_email(cls, email):
        """
        Verify institute email
        """
        username = email.split('@')[0]
        domain = email.split('@')[1]
        if domain not in ['itbhu.ac.in', ]:
            return False
        if '.' not in username:
            return False
        dept_code = cls.get_department_code(email)
        if dept_code not in cls.dept_list:
            return False
        return True


class FirebaseAPI:

    @classmethod
    def verify_id_token(cls, id_token):
        """
        Verify the id token from firebase
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except ValueError as e:
            raise ValidationError(
                'Invalid Firebase ID Token.', HTTP_422_UNPROCESSABLE_ENTITY) from e

    @classmethod
    def delete_user_by_uid(cls, uid):
        """
        Delete User
        """
        auth.delete_user(uid)

    @classmethod
    def get_photo_url(cls, uid):
        """
        Get the photo url of the corresponding user
        """
        # pylint: disable=protected-access
        return auth.get_user(uid)._data['photoUrl']

    @classmethod
    def send_club_message(cls, data, club):
        """
        Gets the message content for Clubs
        """
        topic='C_'+str(club.id)
        if data.get('is_workshop', True):
            msg_notification=messaging.Notification(
                title="New Workshop in "+str(club.name),
                body=data['title']+" on "+str(data['date'].strftime('%d-%m-%Y')),
                image=data.get('image_url',''))
        else:
            msg_notification=messaging.Notification(
                title="New Event in "+str(club.name),
                body=data['title']+" on "+str(data['date'].strftime('%d-%m-%Y')),
                image=data.get('image_url',''))
        message = messaging.Message(
            notification=msg_notification,
            topic=topic
        )

        try:
            response = messaging.send(message)
            logger.info('[Topic %s] Successfully sent message: %s', topic, response)
        except (exceptions.FirebaseError, TransportError) as e:
            logger.warning('[Topic %s] Could not send notification!', topic)
            logger.error(e)

    @classmethod
    def send_entity_message(cls, data, entity):
        """
        Gets the message content for Entities
        """
        topic = 'E_'+str(entity.id)
        if data.get('is_workshop', True):
            msg_notification=messaging.Notification(
                title="New Workshop in "+str(entity.name),
                body=data['title']+" on "+str(data['date'].strftime('%d-%m-%Y')),
                image=data.get('image_url',''))
        else:
            msg_notification=messaging.Notification(
                title="New Event in "+str(entity.name),
                body=data['title']+" on "+str(data['date'].strftime('%d-%m-%Y')),
                image=data.get('image_url',''))
        message = messaging.Message(
            notification=msg_notification,
            topic=topic
        )
        try:
            response = messaging.send(message)
            logger.info('[Topic %s] Successfully sent message: %s', topic, response)
        except (exceptions.FirebaseError, TransportError) as e:
            logger.warning('[Topic %s] Could not send notification!', topic)
            logger.error(e)

    @classmethod
    def send_workshop_update(cls, instance, data):
        """
        Gets the message content on updating workshop or event
        """
        topic = 'W_' + str(instance.id)
        msg_notification = messaging.Notification(
            title=data['title']+" has been updated",
            body='Click here, Don\'t miss any detail',
            image=data.get('image_url',''))
        message = messaging.Message(
            notification=msg_notification,
            topic=topic
        )
        try:
            response = messaging.send(message)
            logger.info('[Topic %s] Successfully sent message: %s', topic, response)
        except (exceptions.FirebaseError, TransportError) as e:
            logger.warning('[Topic %s] Could not send notification!', topic)
            logger.error(e)
