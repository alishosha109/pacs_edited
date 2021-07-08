"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import FileUpload, patient
import dicom
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index2.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    record = FileUpload.objects.all()
    patientObject = patient.objects.all()

    if request.method== "POST":
        file = request.FILES["myfile"]
       # nationalID = request.POST["nationalID"]

        patientID = request.POST.get('dropdown', None)        
        modality = request.POST.get('dropdown2', None)
        patientInformation = patientObject.get(ID= patientID)
        saveFile = FileUpload(dicomImg=file, patientID = patientInformation, modality = modality)
        saveFile.save()


        return render(
            request,
            'app/contact.html',
            {
                'title':'Contact',
                'year':datetime.now().year,
                'message': True,
                'patientObject': patientObject
            }

        )
    else:
        return render(
            request,
            'app/contact.html',
            {
                'title':'Contact',
                'year':datetime.now().year,
                'patientObject': patientObject
            }

        )

def about(request):
    """Renders the about page."""
    record = FileUpload.objects.all()   
    patientObject = patient.objects.all()
    sp_patient = patient.objects.get(ID=1)
    test_list=[]
    test_list_number=[]
    test_list_national=[]
    for item in record:
        test_list.append(patient.objects.get(ID=item.patientID.ID).fullName)
        test_list_number.append(patient.objects.get(ID=item.patientID.ID).phone)
        test_list_national.append(patient.objects.get(ID=item.patientID.ID).nationalID)


    context= {
        'record': record,
        'patientObject': patientObject,
        "sp_patient":sp_patient,
        "test_list":test_list,
        "test_list_number":test_list_number,
        "test_list_national":test_list_national
        }
    return render(
        request,
        'app/about.html',
       # {'title':'About','message':'Your application description page.','year':datetime.now().year,'empty': True,},
        context=context
    )

