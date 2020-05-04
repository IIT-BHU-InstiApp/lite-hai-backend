from django.contrib.auth.models import User

def get_user(username):
    """
    Returns the User instance from the username
    """
    return User.objects.get(username=username)
