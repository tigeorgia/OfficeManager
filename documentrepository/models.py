from django.db import models
from django import forms

class PublicDocument( models.Model ):


    # descriptive name for presentation
    name = models.TextField( max_length = 64 )

    # link to media content
    url = models.TextField( max_length = 1024 )

    # submission date
    date_submitted = models.DateField()


class PublicDocumentForm( forms.ModelForm ):

    file = forms.FileField()
    name = forms.CharField( max_length = 256 )

    class Meta:
        model = PublicDocument
        fields = ['name', 'file', 'id']
        labels = {
                  "name": "Document name",
                  "file": "Upload file",
                  }

