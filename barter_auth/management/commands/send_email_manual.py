from django.core import mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date

from bcapital.settings.base import SENDER_EMAIL, FRONTEND_URL

class Command(BaseCommand):
    help = 'Use this command to send a template to emails'

    def add_arguments(self, parser):
        parser.add_argument('template', type=str, help="Template name. Templates are searched in TEMPLATES.DIRS/emails directories. Don't include extensions in the name")
        parser.add_argument('recipient_list', nargs='+', type=str, help="List of emails to send the template. Separate with space.")
        parser.add_argument('-s', '--silent', action='store_true', dest='is_silent', help='send_mail_test will not raise a SMTPException when things go wrong.')


    def handle(self, *args, **options):
        content = {
            'contact_email': 'soporte@bartercapital-group.com',
            'link_button': f'{FRONTEND_URL}/activate/*',
            'accounts': [ 
                {'service': 'Netflix', 'credential': { 'username':'elliott-dev', 'pswd': ')OW+yf*f,]RrZ8,-' }, 'expire_date': date(2024,3,6) },
                {'service': 'HBOMax', 'credential': { 'username':'elliott-dev', 'pswd': 'M4&LVxD_(XP4<FoP'}, 'expire_date': date(2024,3,6) },
            ],
            'support_link': 'https://bartercapital.atlassian.net/servicedesk/customer/portal/1',
            'kit_plan': 'UltraPremium'
        }
        subject = 'Prueba'
        html_message = render_to_string(f"email/{options['template']}.html", content)
        plain_message = strip_tags(html_message)
        send_to = options['recipient_list']

        mail.send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=SENDER_EMAIL, 
            recipient_list=send_to, 
            fail_silently=options['is_silent'])