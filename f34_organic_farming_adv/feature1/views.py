from django.http import HttpResponse
from django.shortcuts import render


def history(request):
    return render(request,'history.html',{'name1':'History'})

def farming(request):
    return render(request,"farming.html",{'name1':'Farming Information'})

def benfits(request):
    return render(request,"benfits.html",{'name1':'benfits'})

def index(request):
    return render(request,"index.html")
def home(request):
    return render(request,'index.html')
