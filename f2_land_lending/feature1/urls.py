from django.urls import path

from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('templates/index.html',views.index,name='index'),
    path('join_owner',views.join_owner,name='join_owner'),
    path('search_land',views.search_land,name='search_land'),
    path('update_owner_info',views.update_owner_info,name='update_owner_info'),
    path('templates/owner.html',views.owner_registration,name='owner_registration'),
    path('templates/update_owner.html',views.redirect_to_update,name='redirect_to_update'),
    path('templates/customer.html',views.customer,name='customer'),
    path('update_owner',views.update_owner,name='update_owner'),
    path('get_location',views.get_location,name='get_location'),
]
