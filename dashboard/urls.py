from django.urls import path
from dashboard import views
from accounts import views as v

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/<str:username>', v.profile, name='profile'),
    path('update_image/', v.update_image, name='update_image'),
    path('services/add_category_service', views.add_category_service, name='add_category_service'),
    path('services/category_service', views.view_category_service, name='category_service'),
    path('services/edit/<int:service_id>', views.edit_service, name='edit_service'),
    path('service/<int:service_id>', views.service, name='service'),
    path('recipe', views.recipe, name='recipe'),
    path('search', views.search, name='search'),
]