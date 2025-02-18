import json
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Orders
from django.contrib import messages

@csrf_exempt
def Email_invoice(request):
    if request.method == 'POST':
        # Get order id from session
        order_id = request.session.get('order_id', None)
        if not order_id:
            return HttpResponse("Order not found in session.")
        
        # Fetch the order object
        order = Orders.objects.filter(order_id=order_id).first()
        if not order:
            return HttpResponse("Order not found in the database.")

        # Retrieve and parse the items JSON from the POST data
        items_json = request.POST.get('items_json', '')
        try:
            items_data = json.loads(items_json)
        except Exception as e:
            return HttpResponse("Error parsing items data: " + str(e))
        
        # Build the email content
        subject = f"Your Order Confirmation - Order #{order.order_id}"
        message_lines = [
            "Thank you for your order!",
            "",
            f"Order ID: {order.order_id}",
            "Order Details:",
        ]
        grand_total = 0
        for key, value in items_data.items():
            try:
                quantity = value[0]
                product_name = value[1]
                price = value[2]
                line_total = quantity * price
                grand_total += line_total
                message_lines.append(
                    f"{product_name} - Qty: {quantity} - Price: ${price} - Total: ${line_total}"
                )
            except Exception as e:
                message_lines.append(f"Error processing item {key}: {e}")
        
        message_lines.append("")
        message_lines.append(f"Grand Total: ${grand_total}")
        message = "\n".join(message_lines)

        # Get recipient email from the order
        recipient = [order.email]
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(subject, message, from_email, recipient, fail_silently=False)
        except Exception as e:
            messages.success(request, "Failed to send email: " + str(e))
            return redirect('Email_invoice')

        messages.success(request, f"{from_email} Email sent successfully!")
        return redirect('ShopHome')
    else:
        return HttpResponse("Invalid request method.")
