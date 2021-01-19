""" Newsletter views. """

# Django
from django.conf import settings

# Django Rest Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Models
from contact.models import NewsletterContact

# Serializers
from contact.serializers import NewsletterContactModelSerializer

# Utilities
from utils.functions import get_client_ip
from utils.mailchimp import unsubscribe_from_newsletter, resubscribe_to_newsletter, subscribe_to_newsletter
from django_user_agents.utils import get_user_agent
import json


class NewsletterViewset(viewsets.ModelViewSet):
    """ ModelViewset from NewsletterContact model """

    queryset = NewsletterContact.objects.all()
    serializer_class = NewsletterContactModelSerializer

    def create(self, request, *args, **kwargs):
        """ Validates the data from the request and calls perform_create """
        print('====REGULAR CREATE=====')
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid()
        result = False
        try: 
            # Find if the contact already exist, if found, makes sure it's status is ACTIVE
            print('==Check if the contact already exist==')
            contact = NewsletterContact.objects.get(email=request.data['email'])
            print('==It exists, so I change its status to ACTIVE==')
            contact.status = NewsletterContact.NewsletterContactStatus.ACTIVE
            contact.save()
            # reactivate that email from the newsletter list
            result = resubscribe_to_newsletter(contact.email)
        except NewsletterContact.DoesNotExist:
            print('==Does not exist==')
            # The contact doesn't exist on the DB, so I create a new one
            print('==Checking if is valid==')
            serializer.is_valid(raise_exception=True)
            print('== Is valid so I create a new contact')
            result = self.perform_create(serializer)
        
        if result is not True:
            return Response(json.loads(result), status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """ Creates a new newsletter contact adding the user agent and the ip form the request to the DB """
        
        email = serializer.validated_data['email']
        # Add email to list
        result = subscribe_to_newsletter(email)
        if result is not True:
            return result
        print(':::::PERFORM CREATE::::::')
        ip_address = get_client_ip(self.request._request)
        user_agent = get_user_agent(self.request)
        print(ip_address)
        print(user_agent)
        # print('=======USER AGENT!=========')
        # user_agent = get_user_agent(self.request)
        print('========================')
        serializer.validated_data['user_agent'] = user_agent
        serializer.validated_data['ip_address'] = ip_address
        # serializer.is_valid(raise_exception=True)
        serializer.save()
        return True


    @action(detail=False, methods=['put'], url_path='unsubscribe')
    def unsubscribe(self, request, *args, **kwargs):
        """ Set given newsletter contact to INACTIVE """

        try: 
            contact = NewsletterContact.objects.get(pk=request.data['id'])
        except NewsletterContact.DoesNotExist:
            data = {
                'message' : 'Contact not found',
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)        
        
        contact.status = NewsletterContact.NewsletterContactStatus.INACTIVE
        contact.save() 
        result = unsubscribe_from_newsletter(contact.email)
        if result is not True:
            return Response(json.loads(result), status=status.HTTP_400_BAD_REQUEST)
        data = {
            'message' : 'Success',
        }
        return Response(data, status=status.HTTP_200_OK)

     
    