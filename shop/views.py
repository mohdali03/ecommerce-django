from django.shortcuts import redirect, render
from .models import OrderUpdate, Product, Contact, Orders
from math import ceil
import logging

logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    allProds = sorted(allProds, key=lambda x: len(x[0]), reverse=True)


    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken", None)
        print(data)
        contact = Contact(**data)
        contact.save()
    return render(request, 'shop/contact.html')

def checkout(request):
    if request.method =="POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken", None)
        ad1, ad2 = data.pop("address1", None), data.pop("address2", None)
        data["address"] = ad1 + " " + ad2
        
        
        
        
        print(data)
        order = Orders(**data)
        order.save()
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})

    return render(request, 'shop/checkout.html')
def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    product=Product.objects.filter(id=myid).first()
    print(product)
    return render(request, "shop/prodView.html", {'product': product})
