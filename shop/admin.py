from django.contrib import admin
from .models import Contact, OrderUpdate, Product, Orders

class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['product_name', 'price', 'category']
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['order_id', 'amount', 'name', 'email','city']
    
class OrderUpAdmin(admin.ModelAdmin):
    
    list_display = ['order_id','update_id', 'timestamp']
    
class ContactAdmin(admin.ModelAdmin):
    
    list_display = ['msg_id', 'name', 'email', 'phone']

admin.site.register(Orders, OrderAdmin)
admin.site.register(OrderUpdate, OrderUpAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)

# Register your models here.
