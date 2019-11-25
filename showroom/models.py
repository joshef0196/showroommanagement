from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class CustomerRegistration(models.Model):
    name                  = models.CharField(max_length=50)
    email                 = models.EmailField(max_length=80,blank=True)
    mobile1               = models.CharField(max_length=16,blank=True)
    mobile2               = models.CharField(max_length=16,blank=True)
    home_phone            = models.CharField(max_length=16,blank=True)
    nid_number            = models.CharField(max_length=50)
    nid_image             = models.ImageField(upload_to="nid_image/", blank=True)
    present_address       = models.TextField(blank=True)
    permanent_address     = models.TextField(blank=True)
    profession            = models.CharField(max_length=150,blank=True)
    reg_date              = models.DateField(auto_now_add=True)
    status                = models.BooleanField(default=True)

    def __str__(self):
        return self.name+" ("+self.mobile1+")"

    class Meta:
        verbose_name        ='Customer Registration'
        verbose_name_plural ='Customer Registrations'

class ProductCat(models.Model):
    category_name      = models.CharField(max_length=100)
    status             = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name        ='Product Category'
        verbose_name_plural ='Product Categories'

class Product(models.Model):
    category_name               = models.ForeignKey(ProductCat, on_delete=models.CASCADE)
    product_name                = models.CharField(max_length=100)
    brand_name                  = models.CharField(max_length=150, blank=True)
    product_image               = models.ImageField(upload_to="product_image/", blank=True)
    product_model_number        = models.CharField(max_length=100, blank=True)
    product_color               = models.CharField(max_length=50, blank=True)
    available_quantity          = models.IntegerField(default=1)
    total_quantity              = models.IntegerField(default=1)
    unit_price_by_cash          = models.FloatField(default=0)
    unit_price_by_installment   = models.FloatField(default=0)
    total_price                 = models.FloatField(default=0)
    buy_price                   = models.FloatField(default=0)
    maximum_discount            = models.FloatField(default=0, blank=True)
    discription                 = models.TextField(blank=True)
    status                      = models.BooleanField(default=True)

    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name        ='Product'
        verbose_name_plural ='Products'

class CashSalesProduct(models.Model):
    customer             = models.ForeignKey(CustomerRegistration, on_delete=models.CASCADE)
    product              = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_quantity        = models.IntegerField(default=1)
    discount             = models.FloatField(default=0)
    total_price          = models.FloatField(default=0)
    comment              = models.TextField(blank=True)
    sale_date            = models.DateTimeField(auto_now_add=True)
    status               = models.BooleanField(default=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name        ='Sales Product'
        verbose_name_plural ='Sales Products'

class InstallmentSalesProduct(models.Model):
    customer                    = models.ForeignKey(CustomerRegistration, on_delete=models.CASCADE)
    product                     = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_quantity               = models.IntegerField(default=1)
    cash_payment                = models.FloatField(default=0)
    installment_amount_month    = models.FloatField(default=0)
    installment_paid_date       = models.DateTimeField(auto_now_add=False)
    total_price                 = models.FloatField(default=0)
    contact_number              = models.CharField(max_length=16,blank=True)
    comment                     = models.TextField(blank=True)
    sale_date                   = models.DateTimeField(auto_now_add=True)
    status                      = models.BooleanField(default=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name        ='Sales Product'
        verbose_name_plural ='Sales Products'

class Content(models.Model):
    com_name         = models.CharField(max_length=150)
    email            = models.CharField(max_length=50, blank=True)
    mobile1          = models.CharField(max_length=50, blank=True)
    mobile2          = models.CharField(max_length=50, blank=True)
    staring_year     = models.IntegerField()
    address          = models.TextField(max_length=500, blank=True)
    status           = models.BooleanField(default=True)

    def __str__(self):
        return self.com_name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Company Information'

