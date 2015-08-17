from django.shortcuts import render
from documentrepository.models import PublicDocumentForm, PublicDocument
from employee.views import checkuserloggedin, save_file
from OfficeManager import settings
import datetime


@checkuserloggedin
def publicdocuments( request, employee ):

    form = PublicDocumentForm()

    message = ""

    if request.method == 'POST':

        if request.POST['button'] == "Upload":
            target_dir = settings.MEDIA_ROOT + '/publicdocuments'

            if request.FILES.has_key( 'file' ):

                in_file = request.FILES['file']

                save_file( request, target_dir, in_file, employee )

                file_url = settings.MEDIA_URL + "publicdocuments/%s" % ( in_file.name )

                doc_name = request.POST['name']

                if doc_name != '':

                    document = PublicDocument( name = doc_name, url = file_url, date_submitted = datetime.date.today() )
                    document.save()
                else:
                    message += "Please, provide a name for the file<br>"

            else:
                message += "Please, select file to upload<br>"


        if request.POST['button'] == "Delete":

            document = PublicDocument.objects.filter( id = request.POST['id'] )
            document.delete()

    # pylint: disable=no-member
    documents = PublicDocument.objects.all()


    return render( request, "publicdocuments.html",
                   {
                    "employee": employee,
                    "form": form,
                    "message": message,
                    "documents":  documents,
                    } )


