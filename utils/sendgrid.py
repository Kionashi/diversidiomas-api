""" Wrapper of the sendgrid library to send emails"""

# Django
from django.conf import settings

# Sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_email_with_template(email_form,email_to,subject,template_id,data):
    """ Send email with given data """
    message = Mail(
    from_email=email_form,
    to_emails=email_to,
    subject=subject,
    )
    message.dynamic_template_data = data
    message.template_id = template_id
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(e)
        return e

    

def send_contact_form_email(data):
    """ Wrapper from send_email_with_template to make easier to send emails with the contact form data"""
    return send_email_with_template('cardozo.anibal@gmail.com','cardozo.anibal@gmail.com','Contact form',os.environ.get('SENDGRID_CONTACT_TEMPLATE'),data)

    