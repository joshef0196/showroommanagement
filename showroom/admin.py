from django.contrib import admin
from .import models
from django.utils.html import format_html

admin.site.register(models.CustomerRegistration)
admin.site.register(models.ProductCat)
admin.site.register(models.Product)
admin.site.register(models.SaleProducts)
admin.site.register(models.InstallmentCollection)
admin.site.register(models.Content)
admin.site.register(models.Branches)