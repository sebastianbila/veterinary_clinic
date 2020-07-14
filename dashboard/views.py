from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.models import ClinicServices, CategoryServices, Recipe
from patients.models import ClinicPatients
from receipt.models import Receipt


def dashboard(request):
    if request.user.is_authenticated:
        services_all = Receipt.objects.all()
        full_sum = 0
        for item in services_all:
            full_sum = full_sum + item.full_price

        context = {
            'patient_count': len(ClinicPatients.objects.all()),
            'recipe_count': len(Recipe.objects.all()),
            'service_count': len(services_all),
            'balance': full_sum
        }
        return render(request, 'pages/dashboard/dashboard.html', context)
    else:
        return render(request, 'pages/auth/login.html')


def add_category_service(request):
    if request.method == "POST":
        service_id = request.POST['clinic-services']
        title = request.POST['service_title']
        price = request.POST['service_price']

        service_category = CategoryServices.objects.create(
            service=ClinicServices.objects.get(id=service_id),
            title=title,
            price=price
        )

        service_category.save()
        messages.success(request, 'Категория была добавлена')
        return redirect('category_service')
    else:
        services = ClinicServices.objects.all()
        context = {
            'services': services
        }
        return render(request, 'pages/services/add_category_service.html', context)


def view_category_service(request):
    services = ClinicServices.objects.all()
    category_services = CategoryServices.objects.all()

    if request.is_ajax():
        print("Ajax request")
        service_id = int(request.POST['service_id'])

        if service_id != -1:
            category_services = CategoryServices.objects.all().filter(service_id=service_id)
            print(category_services)
        else:
            category_services = category_services

        data = {
            'category_services': list(category_services.values())
        }
        return JsonResponse(data, safe=False)
    else:
        context = {
            'services': services,
            'category_services': category_services
        }
        return render(request, 'pages/services/category_service.html', context)


def edit_service(request, service_id):
    category_service = get_object_or_404(CategoryServices, id=service_id)

    if request.method == "POST":
        category_service.service = request.POST['clinic-services']
        category_service.title = request.POST['service_title']
        category_service.price = request.POST['service_price']
        category_service.save()
        messages.success(request, 'Даные успешно изменены')
        return redirect('category_service')

    return render(request, 'pages/services/edit_category_service.html', {'service': category_service})


def service(request, service_id):
    return HttpResponse("Hello")


def recipe(request):
    if request.is_ajax():
        # Save recipe
        text = request.POST['recipe-content']
        print(text)
        new_recipe = Recipe.objects.create(
            text=text
        )
        new_recipe.save()
        return JsonResponse({'status': True})
    return render(request, 'pages/recipe/recipe.html')


def search(request):
    results = []

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            search_vector = SearchVector('nickname', 'description', 'owner', 'patient_type')
            search_query = SearchQuery(keywords)
            results = ClinicPatients.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')

    context = {
        'patients': results,
    }
    return render(request, 'pages/search/search.html', context)
