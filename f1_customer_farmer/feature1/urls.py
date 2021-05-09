from django.urls import path

from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    path('join_farmer',views.join_farmer,name='join_farmer'),
    path('check',views.check,name='check'),
    path('search_farmer',views.search_farmer,name='search_farmer'),
    path('update_farmer_info',views.update_farmer_info,name='update_farmer_info'),
    path('templates/farmer.html',views.Farmer_registration,name='Farmer_registration'),
    path('templates/update_farmer.html',views.redirect_to_update,name='redirect_to_update'),
    path('templates/customer.html',views.customer,name='customer'),
    
    path('templates/index.html',views.index,name='index'),

    path('update_farmer',views.update_farmer,name='update_farmer'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('get_location',views.get_location,name='get_location'),
]
