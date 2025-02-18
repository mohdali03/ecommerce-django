
from django.urls import path
from . import views
from .email import send_order_email 

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    # path('hadlerequest/', views.handlerequest, name="handler")
    path('paymentsuccess/', views.paymentsuccess, name='paymentsuccess'),
    path('send_order_email/', send_order_email, name='send_order_email'),

    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

]

