from tickets.models import User
from django.contrib.auth import get_user_model

def authentificate(username, password):
    User = get_user_model()
    try:
        user = User.objects.get(username = username)
        print(user.id)
        return user.check_password(raw_password = password)
    except User.DoesNotExist:
        return False