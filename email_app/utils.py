from django.core.mail import send_mail
from django.template.loader import render_to_string

# * Currently only the bartercapital-dashboard.com Domain
# * Is verified on AWS SES
# * If sending from another domain
# * Remember to add it in the verified identities section
NO_REPLY_EMAIL = "Barter Capital <no-reply@bartercapital-dashboard.com>"
SUPPORT_EMAIL = "Soporte - Barter Capital <soporte@bartercapital-dashboard.com>"


def send_sales_funnel_welcome_email(user_email: str):
    subject = "Bienvenido a Barter Capital"
    message = render_to_string(
        "email_app/public/sales_funnel_subscription_welcome_plain.txt"
    )
    html_message = render_to_string(
        "email_app/public/sales_funnel_subscription_welcome.html"
    )
    send_mail(subject, message, NO_REPLY_EMAIL, [user_email], html_message=html_message)
