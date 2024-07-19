from datetime import timedelta

from cryptography.fernet import Fernet
from django.core import mail
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from barter_auth.enums import TokenTypesEnum
from barter_auth.models import BarterUser, VerificationActions
from bcapital.settings.base import SENDER_EMAIL, FRONTEND_URL, SUPPORT_EMAIL

key = Fernet.generate_key()
fernet = Fernet(key=key)
import base64


def send_activate_user(user: BarterUser):
    """
    Send email to activate user email_verification.html
    @type user: BarterUser
    """

    token = fernet.encrypt(b'' + str(user.id).encode('utf-8'))
    verification_action = VerificationActions.objects.create(
        user=user,
        token=token,
        type=TokenTypesEnum.VERIFICATION.value,
        expiration_date=timezone.now() + timedelta(days=1)
    )
    verification_action.save()
    url = f'{FRONTEND_URL}/auth/activate/?key={token.decode("utf-8")}'
    contact_email = SUPPORT_EMAIL
    content = {
        'contact_email': contact_email,
        'link_button': url
    }
    subject = 'Activa tu cuenta'
    html_message = render_to_string(f"email/email_verification.html", content)
    plain_message = strip_tags(html_message)
    send_to = [user.email]
    mail.send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email=SENDER_EMAIL,
        recipient_list=send_to,
        fail_silently=True)


def activate_user(token: str):
    """
    Activate user by token email_notification.html
    @type token: str
    """
    
    # since we sent a decoded token as a URL Parameter
    # on line 33, we have to encode it again
    encoded_token = token.encode('utf-8')
    
    try:
        verification_action = VerificationActions.objects.get(token__exact=encoded_token)
    except VerificationActions.DoesNotExist:
        return False
    
    if verification_action.expiration_date < timezone.now() or verification_action.used:
        return False
    
    try:
        user = BarterUser.objects.get(pk=verification_action.user.id)
    except BarterUser.DoesNotExist:
        return False
    
    user.verified = True
    user.save()
    
    verification_action.used = True
    verification_action.save()
    
    #region sent verified email
    contact_email = SUPPORT_EMAIL
    content = {
        'contact_email': contact_email,
        'support_link': SUPPORT_EMAIL,
    }
    
    subject = 'Bienvenido a Barter'
    html_message = render_to_string(f"email/email_notification.html", content)
    plain_message = strip_tags(html_message)
    send_to = [user.email]

    mail.send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email=SENDER_EMAIL,
        recipient_list=send_to,
        fail_silently=True)
    #endregion
    
    return True


def send_recovery_password(user: BarterUser):
    # pswd_recovery.html
    token = fernet.encrypt(b'' + str(user.id).encode('utf-8'))
    verification_action = VerificationActions.objects.create(
        user=user,
        token=token,
        type=TokenTypesEnum.RECOVERY_PASSWORD.value,
        expiration_date=timezone.now() + timedelta(days=1)
    )

    url = f'{FRONTEND_URL}/auth/reset-password/?key={token.decode("utf-8")}'
    contact_email = SUPPORT_EMAIL

    content = {
        'contact_email': contact_email,
        'link_button': url
    }

    subject = 'Recuperar contraseña'
    html_message = render_to_string(f"email/pswd_recovery.html", content)
    plain_message = strip_tags(html_message)
    send_to = [user.email]

    verification_action.save()

    mail.send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email=SENDER_EMAIL,
        recipient_list=send_to,
        fail_silently=True)


def recover_password(token, password):
    # pswd_notification.html
    try:
        token = token.encode('utf-8')
        verification_action = VerificationActions.objects.get(token=token)
        if verification_action.expiration_date < timezone.now() or verification_action.used \
                or verification_action.type != TokenTypesEnum.RECOVERY_PASSWORD.value:
            return False
        user = verification_action.user
        user.set_password(password)
        user.save()
        verification_action.used = True
        verification_action.save()

        contact_email = SUPPORT_EMAIL

        content = {
            'contact_email': contact_email,
        }
        subject = 'Contraseña cambiada'

        html_message = render_to_string(f"email/pswd_notification.html", content)
        plain_message = strip_tags(html_message)
        send_to = [user.email]

        mail.send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=SENDER_EMAIL,
            recipient_list=send_to,
            fail_silently=True)
        return True
    except VerificationActions.DoesNotExist:
        return False
