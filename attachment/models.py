from django.db import models
from django.db.models.fields.related import ForeignKey
from employee.models import Profile 

# a profile attachment (scanned document, link)

class ProfileAttachment( models.Model):
    
    profile = ForeignKey( Profile)
    name = models.TextField( max_length = 512)
    url = models.TextField( max_length = 1024)
    created = models.DateField( null = True)

    