from django.db import models
from django.db.models.fields.related import ForeignKey
from employee.models import Profile 

# a profile attachment (scanned document, link)

class ProfileAttachment( models.Model):
    
    profile = ForeignKey( Profile)
    name = models.TextField( max_length = 512)
    link = models.TextField( max_length = 1024)
    file = models.FileField( upload_to = "attachments", max_length = 512)

    