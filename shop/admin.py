from django.contrib import admin
from .models import Contact, OrderUpdate, Product, Orders
from django.utils.html import format_html
from django.contrib.admin import DateFieldListFilter

from import_export.admin import ImportExportModelAdmin

from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    
    list_display = ['product_image','product_name', 'price', 'category', 'qty']
    search_fields = ['product_name', 'price', 'category', 'qty']
    list_filter = [('pub_date', DateRangeFilterBuilder()) , 'price', 'category', 'qty' ]
    def product_image(self,obj):
        if obj.image:
            return format_html('<img src="{}" width="75" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    
    
    product_image.short_description = 'image'
    
@admin.register(Orders)
class OrderAdmin(ImportExportModelAdmin):
    
    list_display = ['order_id', 'amount', 'name', 'email','city']
    search_fields= ['order_id', 'amount', 'name', 'email','city']
    list_filter = ['amount', 'city']
@admin.register(OrderUpdate)
class OrderUpAdmin(ImportExportModelAdmin):
    
    list_display = ['order_id','update_id', 'timestamp']
    list_filter = [('timestamp', DateTimeRangeFilterBuilder())]
    search_fields = ['order_id','update_id', 'timestamp']
    
@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    
    list_display = ['msg_id', 'name', 'email', 'phone']
    search_fields = ['msg_id', 'name', 'email', 'phone']


# Register your models here.
