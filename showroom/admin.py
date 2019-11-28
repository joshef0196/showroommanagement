from django.contrib import admin
from .import models
from django.utils.html import format_html

class ProductCatAdmin(admin.ModelAdmin):
    list_display    = ['branch','category_name','status']
    list_filter     = ['branch','status']

class CustomerRegistrationAdmin(admin.ModelAdmin):
    list_display    = ['branch','name','mobile','present_address','reference_person','status']
    list_filter     = ['branch','status']

class ProductAdmin(admin.ModelAdmin):
    list_display    = ['branch','category_name','product_name','unit_price_by_cash','unit_price_by_installment','available_quantity','status']
    list_filter     = ['branch','status']

class SaleProductsAdmin(admin.ModelAdmin):
    list_display    = ['branch','customer','product','payment_type','status']
    list_filter     = ['branch','status']

admin.site.register(models.CustomerRegistration, CustomerRegistrationAdmin)
admin.site.register(models.ProductCat, ProductCatAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.SaleProducts, SaleProductsAdmin)
admin.site.register(models.InstallmentCollection)
admin.site.register(models.Content)
admin.site.register(models.Branches)