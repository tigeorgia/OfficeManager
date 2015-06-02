from django.db import models

class PublicHoliday( models.Model):
    
    date = models.DateField()
    name = models.TextField( max_length = 256)
    type = models.TextField( max_length = 256)
