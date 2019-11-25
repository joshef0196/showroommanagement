from django.contrib import admin
from .import models
from django.utils.html import format_html

# class RegistrationAdmin(admin.ModelAdmin):
#     list_display    = ['name','email','mobile','reg_date','status']
#     search_fields   = ['name','email','mobile','reg_date','status']
#     list_filter     = ['name','status']

# class ProductCatAdmin(admin.ModelAdmin):
#     list_display    = ['category_name','status']
#     search_fields   = ['category_name','status']
#     list_filter     = ['category_name','status']

# class ProductAdmin(admin.ModelAdmin):
#     list_display    = ['category_name','product_name','brand_name','available_quantity','total_quantity','product_color','product_model_number','unit_price','total_price','status']
#     search_fields   = ['category_name_id__category_name','product_name','status']
#     list_filter     = ['category_name','product_name','status']

# class SalesProductAdmin(admin.ModelAdmin):
#     list_display    = ['salesman','product','sale_quantity','discount','sale_date','status']
#     search_fields   = ['salesman_id__name','product_id__product_name','discount','status']
#     list_filter     = ['salesman','salesman','status']

# class ContentAdmin(admin.ModelAdmin):
#     list_display    = ['com_name','staring_year','status']
#     search_fields   = ['com_name','status']
#     list_filter     = ['com_name','status']

admin.site.register(models.CustomerRegistration)
admin.site.register(models.ProductCat)
admin.site.register(models.Product)
admin.site.register(models.CashSalesProduct)
admin.site.register(models.InstallmentSalesProduct)
admin.site.register(models.Content)