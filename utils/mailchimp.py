""" Mailchimp wrapper to simplify the main functions of the API"""
import os

# Django
from django.conf import settings

# Mailchimp API
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Utils
import hashlib

API_KEY = os.environ.get('MAILCHIMP_API_KEY')
SERVER = os.environ.get('MAILCHIMP_SERVER')
NEWSLETTER_LIST_ID = os.environ.get('MAILCHIMP_NEWSLETTER_LIST_ID')

def subscribe_to_list(list_id, email, merge_fields={}):
    """ Adds a contact/member to a given mailchimp audience/list """

    mailchimp = Client()
    mailchimp.set_config({
    "api_key": API_KEY,
    "server": SERVER
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": merge_fields
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
        return True
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return format(error.text)

def edit_subscription_from_list(list_id, email, status):
    """ Edit the status from an already created contact/member to a given audience/list. status must be subscribed or unsubscribed """
    mailchimp = Client()
    mailchimp.set_config({
    "api_key": API_KEY,
    "server": SERVER
    })
 
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    member_update = {"status": status}

    try:
        response = mailchimp.lists.update_list_member(list_id, email_hash, member_update)
        print("Response: {}".format(response))
        return True
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return format(error.text)

def subscribe_to_newsletter(email):
    """Wrapper from subscribe_to_list to add people to a newsletter """
    return subscribe_to_list(NEWSLETTER_LIST_ID, email)

def unsubscribe_from_newsletter(email):
    """Wrapper from subscribe_to_list to add people to a newsletter """
    return edit_subscription_from_list(NEWSLETTER_LIST_ID, email, 'unsubscribed')

def resubscribe_to_newsletter(email):
    """ Edit the status of an already added member from the newsletter so it is subscribed again """
    return edit_subscription_from_list(NEWSLETTER_LIST_ID, email, 'subscribed')
    



        