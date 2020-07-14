import json

from django.shortcuts import render, redirect

from dashboard.models import CategoryServices
from patients.models import ClinicPatients
from receipt.models import Receipt


def receipt(request):
    category_services = CategoryServices.objects.all()
    patients = ClinicPatients.objects.all()

    context = {
        'services': category_services,
        'patients': patients
    }

    if request.is_ajax():
        patient = request.POST['patient']
        full_price = request.POST['full_price']
        data = json.loads(request.POST.get('services'))

        services = ", "
        services = services.join(data)

        full_receipt = Receipt.objects.create(
            name=patient,
            list_services=services,
            full_price=full_price
        )

        full_receipt.save()
        return redirect('dashboard')
    return render(request, 'pages/receipt/create_receipt.html', context)

