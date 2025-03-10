
from django.urls import path
from . import views
from .email import Email_invoice 

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path('paymentsuccess/', views.paymentsuccess, name='paymentsuccess'),
    path('Email_invoice/', Email_invoice, name='Email_invoice'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]

