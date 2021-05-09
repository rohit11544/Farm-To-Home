from django.urls import path

from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    path('templates/history.html',views.history,name='history'),
    path('templates/farming.html',views.farming,name='farming'),
    path('templates/benfits.html',views.benfits,name='benfits'),
    path('templates/index.html',views.index,name='index'),
]
