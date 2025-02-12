from django.shortcuts import render
from .models import Product
from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    product = Product.objects.all()
    print(product)
    n = len(product)
    nSlides = n//4 + ceil((n/4)-(n/4))
    params = {"no_of_sildes": nSlides, "range": range(1,nSlides), "product": product}
    
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return HttpResponse("We are at contact")

def tracker(request):
    return HttpResponse("We are at tracker")

def search(request):
    return HttpResponse("We are at search")

def productView(request):
    return HttpResponse("We are at product view")

def checkout(request):
    return HttpResponse("We are at checkout")
