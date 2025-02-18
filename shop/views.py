import json
from django.shortcuts import redirect, render
from django.conf import settings

from .forms import CheckoutForm

from .models import OrderUpdate, Product, Contact, Orders
from math import ceil
from django.views.decorators.csrf import csrf_exempt
import logging
import razorpay
from django.http import HttpResponse
from django.core.mail import send_mail

logger = logging.getLogger(__name__)
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def index(request):

    allProds = []
    catprods = Product.objects.values('category', 'id')
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
    print(params)
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
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                amount_int = data.get('amount')
            except (ValueError, TypeError):
                return HttpResponse("Invalid amount")
            razorpay_amount = amount_int * 100  # Convert INR to paise

            currency = 'INR'
            razorpay_order = razorpay_client.order.create({
                'amount': razorpay_amount,
                'currency': currency,
                'payment_capture': '0'
            })
            razorpay_order_id = razorpay_order['id']

            # Create the order (commit=False allows us to set additional fields)
            order = form.save(commit=False)
            order.address = data.get('address')  # Combined address
            order.amount = amount_int  # Save the amount in INR (if your model stores INR)
            order.save()

            # Create an order update record
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()

            context = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                'razorpay_amount': razorpay_amount,  # in paise
                'currency': currency,
                'callback_url': 'http://127.0.0.1:8000/paymenthandler/',  # Ensure this URL is correct
                'order_id': order.order_id,
            }
            print(context)
            return render(request, 'shop/paytm.html', context=context)
        else:
            # If form is invalid, render the checkout page with errors
            return render(request, 'shop/checkout.html', {'form': form})
    else:
        form = CheckoutForm()
    return render(request, 'shop/checkout.html', {'form': form})
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            print(request.POST.dict())
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print("Params for signature verification:", params_dict)
        
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                print("Signature verification successful")
            except Exception as e:
                print("Signature verification failed:", e)
                return render(request, 'shop/paymentfail.html')
            amount = request.POST.get('razorpay_amount', None)
            if not amount:
                return HttpResponse("Amount not found")
            amount = int(amount)
            
            try:
                razorpay_client.payment.capture(payment_id, amount)
                print("Capture successful")
                
                order_id = request.POST.get('order_id', '')

                print("Order ID:", order_id)

                order = Orders.objects.filter(order_id=order_id).first()
                if order:
                    print("Order:", order)

                request.session['order_id'] = order_id               
                return redirect('paymentsuccess')
            except Exception as e:
                print("Capture failed:", e)
                return render(request, 'shop/paymentfail.html')
    
        except Exception as e:
            print("Error in paymenthandler:", e)
            return HttpResponse("This is bad")
    else:
        return HttpResponse("failed")
    
    
def paymentsuccess(request):
    order_id = request.session.get('order_id', None)
    if order_id:
        order = Orders.objects.filter(order_id=order_id).first()
        original_items_json = order.items_json
        items_list = []
        total_amount = 0
        if original_items_json:
            try:
                items_data = json.loads(original_items_json)
                for key, value in items_data.items():
                    quantity = value[0]
                    product_name = value[1]
                    price = value[2]
                    line_total = quantity * price
                    items_list.append({
                        'quantity': quantity,
                        'product_name': product_name,
                        'price': price,
                        'total': line_total,
                    })
                    prod = Product.objects.filter(product_name=product_name).first()
                    if prod:
                        prod.qty = max(0, prod.qty - quantity)
                        prod.save()
                    total_amount += line_total
                # Return AFTER processing all items
                return render(request, 'shop/paymentsuccess.html', {
                    'order': order,
                    'items': items_list,
                    'total_amount': total_amount,
                    'original_items_json': original_items_json,
                })
            except Exception as e:
                print("Error parsing items_json:", e)
    else:
        order = None
    return render(request, 'shop/paymentsuccess.html', {'order': order})
  
    

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []

                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps([updates, order[0].items_json], default=str)
                print(response)
                return HttpResponse(response)
            
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')



def search(request):
    return render(request, 'shop/search.html')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def productView(request, myid):
    product = Product.objects.get(id=myid)
    print(product)
    similar_products = list(Product.objects.filter(category=product.category).exclude(id=product.id))
    similar_groups = list(chunks(similar_products, 4))
    return render(request, "shop/prodView.html", {
        'product': product,
        'similar_groups': similar_groups,
    })
