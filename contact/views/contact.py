""" View that holds the logic behind the contact form """
# Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Utilities
import string
import random
from utils.sendgrid import *
from utils.sendinblue import send_contact_email

@api_view(['POST'])
def send_contact(request):

    data = {
        'name' : request.data['name'],
        'email' : request.data['email'],
        'message' : request.data['message'],
    }    
    result = send_contact_email(data)
    
    return Response(data, status=status.HTTP_201_CREATED)