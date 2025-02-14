from django.contrib import admin
from .models import Contact, OrderUpdate, Product, Orders

class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['product_name', 'price', 'category']

admin.site.register(Orders)
admin.site.register(OrderUpdate)

admin.site.register(Product, ProductAdmin)
admin.site.register(Contact)

# Register your models here.
