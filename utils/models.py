""" Django models utilities. """

# Django
from django.db import models

class BaseModel(models.Model):
    """ Base model. """
    
    created = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text='Date time on witch the object was created'
    )
    modified = models.DateTimeField(
        'modified_at',
        auto_now=True,
        help_text='Date time on witch the object was last modified'
    )
    
    class Meta:
        """ Meta options."""

        abstract = True
        
        get_latest_by = 'created'
        ordering = ['-created', '-modified']


