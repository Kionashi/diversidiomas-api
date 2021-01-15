""" Newsletter Models """

# Django
from django.db import models

# Utilities
from utils.models import BaseModel
 
class NewsletterContact(BaseModel):
    """ Newsletter contact model. """
    email = models.EmailField(name="email", max_length=50, unique=True)
    ip_address = models.CharField(max_length=20, null=True, blank=True)
    user_agent = models.CharField(max_length=50, null=True, blank=True)
    class NewsletterContactStatus(models.TextChoices):
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'
    status = models.CharField(choices=NewsletterContactStatus.choices, default=NewsletterContactStatus.ACTIVE,  max_length=10)
    class Meta():
        """Meta class."""
        db_table = 'newsletter_contacts'


