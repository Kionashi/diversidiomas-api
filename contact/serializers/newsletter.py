""" Newsletter Serializers. """

# Django rest framework
from rest_framework import serializers

# Models
from contact.models import NewsletterContact

class NewsletterContactModelSerializer(serializers.ModelSerializer):
    """ Newsletter contact model serializer. """
    
    class Meta(): 
        """ Meta class. """
        model = NewsletterContact
        fields = (
            'id',
            'email',
            'ip_address',
            'user_agent',
            'status'
        )