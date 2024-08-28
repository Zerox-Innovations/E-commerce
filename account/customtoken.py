from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from datetime import datetime, timedelta
import jwt

def generate_password_reset_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token




from django.core.mail import EmailMessage


def send_password_reset_email(user,token):
    reset_link = f"{settings.BACKEND_URL}/confirmpassword/{token}/"
    subject = "Password Reset Request"
    sender = settings.EMAIL_HOST_USER
    recipient_list =  [user.email]
    print(recipient_list,'recipeeeeeeeee')
    message = f"Hi {user.first_name},\n\nTo reset your password, click the link below:\n\n{reset_link}\n\nIf you did not request a password reset, please ignore this email."
   
    email = EmailMessage(subject, message, sender, recipient_list)
    email.send()


# def send_password_reset_email(user, token):
#     reset_link = f"{settings.BACKEND_URL}/confirmpassword/{token}/"
#     subject = "Password Reset Request"
#     sender = [user.email]
#     recipient_list =  settings.EMAIL_HOST_USER
#     print(recipient_list,'recipeeeeeeeee')
#     message = f"Hi {user.first_name},\n\nTo reset your password, click the link below:\n\n{reset_link}\n\nIf you did not request a password reset, please ignore this email."
#     send_mail(subject, message, recipient_list, sender)

from rest_framework.exceptions import ValidationError

def decode_password_reset_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise ValidationError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValidationError('Invalid token')