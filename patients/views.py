import urllib

from django.contrib import messages
from django.core.files import File
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from patients.forms import PatientForm
from patients.models import ClinicPatients


def patients(request):
    client_patients = ClinicPatients.objects.all().order_by('id')

    paginator = Paginator(client_patients, 10)
    page = request.GET.get('page')
    paged_patients = paginator.get_page(page)

    context = {
        'patients': paged_patients,
    }
    return render(request, 'pages/patients/patients.html', context)


def add_patients(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        patient_photo = request.FILES['patient-photo']
        owner = request.POST['owner']
        patient_type = request.POST['patient_type']

        patient = ClinicPatients.objects.create(
            nickname=name,
            image=patient_photo,
            description=description,
            owner=owner,
            patient_type=patient_type
        )

        patient.save()
        return redirect('patients')
    return redirect('patients')


def get_patient(request):
    if request.is_ajax():
        patient_id = request.POST['patient_id']
        patient = ClinicPatients.objects.get(id=patient_id)
        try:
            context = {
                'id': patient.id,
                'name': patient.nickname,
                'image': patient.image.url,
                'description': patient.description,
                'owner': patient.owner,
                'type': patient.patient_type
            }

            return JsonResponse({'patient': context})
        except ValueError:
            return JsonResponse({'patient': False})

    return JsonResponse({'status': False})


def save_patient(request):
    if request.method == 'POST':
        patient_id = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        owner = request.POST['owner']
        patient_type = request.POST['patient_type']
        patient = get_object_or_404(ClinicPatients, id=patient_id)

        try:
            file = request.FILES['selected-file']
            patient.image = file
        except MultiValueDictKeyError:
            print('No file selected')

        patient.nickname = name
        patient.description = description
        patient.owner = owner
        patient.patient_type = patient_type
        patient.save()
        messages.success(request, 'Успішно змінено')
    return redirect('patients')


def delete_patient(request):
    if request.is_ajax():
        patient_id = request.POST['id']
        ClinicPatients.objects.get(id=patient_id).delete()
    return redirect('patients')
