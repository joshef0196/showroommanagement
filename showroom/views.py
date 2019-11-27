from django.shortcuts import render, redirect, HttpResponse
from . import models
from django.contrib import messages
from django.db.models import F, Q, Sum
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
import datetime, hashlib, socket, string, os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.dateparse import parse_date, parse_datetime

def index(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    return render(request, "showroom/admin/index.html") 

def login(request):
    brance = models.Branches.objects.filter(status = True)
    context = {
        'brance' : brance,
    }
    if request.method=="POST":
        username  = request.POST['username']
        password  = request.POST['password']

        user      = User.objects.filter(username = username).first()
        if user:
            pwd_valid = check_password(password, user.password)
            if pwd_valid:
                request.session['user'] = user.username
                request.session['usertype'] = 'admin'
                return redirect("/dashboard/")
        else:
            messages.error(request,'* Email and Password incorrect.')
            return redirect("/admin/")

    return render(request, "showroom/login.html", context)

def logout(request):  
    request.session['user'] = False
    request.session['usertype'] = False
    return redirect('/admin/')

def add_product_cat(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    brance_list      = models.Branches.objects.all()
    context={
        'brance_list' : brance_list,
    }
    if request.method=="POST":
        branch_name     = request.POST['branch_name']
        category_name   = request.POST['category_name']

        if models.ProductCat.objects.create(branch_id = branch_name, category_name = category_name,  ):
            messages.success(request,'Category setup successfully!')
            return redirect("/product-category-add/")
        else:
            messages.error(request,"Please enter a valid value.") 
            return redirect("/product-category-add/")

    return render(request,"showroom/admin/add_product_cat.html",context)

def edit_product_cat(request, id):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    edit_product_cat   = models.ProductCat.objects.filter(id = id).first()
    branch             = models.Branches.objects.filter(status = True).exclude(id = edit_product_cat.branch_id)
    context={
        'edit_product_cat' : edit_product_cat,
        'branch' : branch,
    }
    if request.method=="POST":
        branch_name     = request.POST['branch_name']
        category_name   = request.POST['category_name']

        if models.ProductCat.objects.filter(id = id).update(branch_id = branch_name, category_name = category_name):
            messages.success(request,'Successfully updated.')
            return redirect("/category-list/")
        else:
            messages.error(request,"Please enter a valid value.") 
            return redirect("/category-list/")

    return render(request,"showroom/admin/edit_product_cat.html",context)

def delete_pro_category (request, id):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    models.ProductCat.objects.filter(id = id).delete()
    return redirect('/category-list/')

def category_list (request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    cat_list      = models.ProductCat.objects.all()
    context={
        'cat_list' : cat_list,
    }
    return render(request, "showroom/admin/cat_list.html", context)

def add_branch(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    if request.method=="POST":
        brance_name         = request.POST['brance_name']
        proprietor_name     = request.POST['proprietor_name']
        username            = request.POST['username']
        password            = request.POST['password']
        email               = request.POST['email']
        mobile              = request.POST['mobile']
        staring_year        = request.POST['staring_year']
        address             = request.POST['address']

        new_md5_obj     = hashlib.md5(password.encode())
        new_enc_pass    = new_md5_obj.hexdigest()
        if models.Branches.objects.create( branch_name = brance_name, user_name = username, password = new_enc_pass, proprietor_name= proprietor_name, email = email, mobile = mobile, staring_year = staring_year, address = address ):
            messages.success(request,'Brance setup successfully!')
            return redirect("/add-brance/")
        else:
            messages.error(request,"Please enter a valid value.") 
            return redirect("/add-brance/")

    return render(request,"showroom/admin/add_brance.html")

def edit_branch(request, id):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    edit_branch = models.Branches.objects.filter( id = id ).first()
    context = {
        'edit_branch' : edit_branch
    }
    if request.method=="POST":
        brance_name         = request.POST['brance_name']
        proprietor_name     = request.POST['proprietor_name']
        username            = request.POST['username']
        email               = request.POST['email']
        mobile              = request.POST['mobile']
        staring_year        = request.POST['staring_year']
        address             = request.POST['address']

        if models.Branches.objects.filter(id = id).update( branch_name = brance_name, user_name = username, proprietor_name= proprietor_name, email = email, mobile = mobile, staring_year = staring_year, address = address ):
            messages.success(request,'Successfully updated.')
            return redirect("/branch-list/")
        else:
            messages.error(request,"Please enter a valid value.")
            return redirect("/branch-list/")

    return render(request,"showroom/admin/edit_branch.html", context)

def delete_branch (request, id):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    models.Branches.objects.filter(id = id).delete()
    return redirect('/branch-list/')

def branch_list (request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    brance_list      = models.Branches.objects.all()
    context={
        'brance_list' : brance_list,
    }
    return render(request, "showroom/admin/branch_list.html", context)

def add_product(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    brance_list      = models.Branches.objects.all()
    pro_cat          = models.ProductCat.objects.all()
    context={
        'brance_list' : brance_list,
        'pro_cat'     : pro_cat,
    }
    if request.method=="POST":
        category_name               = request.POST['category_name']
        branch_name                 = request.POST['branch_name']
        product_name                = request.POST['product_name']
        brand_name                  = request.POST['brand_name']
        product_model_number        = request.POST['product_model_number']
        product_color               = request.POST['product_color']
        total_quantity              = request.POST['total_quantity']
        unit_price_by_cash          = request.POST['unit_price_by_cash']
        unit_price_by_installment   = request.POST['unit_price_by_installment']
        buy_price                   = request.POST['buy_price']
        maximum_discount            = request.POST['maximum_discount']
        discription                 = request.POST['discription']
        total_price                 = round((int(total_quantity)*float(unit_price_by_cash)),2)

        order_file1 = ""
        if bool(request.FILES.get('product_image', False)) == True:
            file = request.FILES['product_image']
            order_file1 = "product_image/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT):
                os.mkdir(settings.MEDIA_ROOT)
            if not os.path.exists(settings.MEDIA_ROOT+"product_image/"):
                os.mkdir(settings.MEDIA_ROOT+"product_image/")
            default_storage.save(settings.MEDIA_ROOT+"product_image/"+file.name, ContentFile(file.read()))
        
        if models.Product.objects.create( category_name_id = category_name, branch_id = branch_name, product_name = product_name, brand_name = brand_name,
                product_image = order_file1, product_model_number = product_model_number, product_color = product_color, total_quantity = total_quantity, available_quantity = total_quantity,
                unit_price_by_cash = unit_price_by_cash, unit_price_by_installment = unit_price_by_installment, buy_price = buy_price, maximum_discount = maximum_discount,
                total_price = total_price, discription = discription
            ):
            messages.success(request,'Product added successfully!')
            return redirect("/add-product/")
        else:
            messages.error(request,"Please enter a valid value.") 
            return redirect("/add-product/")

    return render(request,"showroom/admin/add_product.html",context)

def product_list (request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    product_list      = models.Product.objects.filter(status = True)
    context={
        'product_list' : product_list,
    }
    return render(request, "showroom/admin/product_list.html", context)

# ...........For Branch .........
def branch_dashboard(request):
    if not request.session['id']:
        return redirect('/login/')
    
    return render(request,'showroom/branch/index.html')

def branch_login(request):
    brance = models.Branches.objects.filter(status = True)
    context = {
        'brance' : brance,
    }
    if request.method=="POST":
        username  = request.POST['username']
        password  = request.POST['password']

        new_md5_obj = hashlib.md5(password.encode())
        enc_pass    = new_md5_obj.hexdigest()
        user  = models.Branches.objects.filter(user_name = username, password = enc_pass)
        if user:
            request.session['id'] = user[0].id
            request.session['proprietor_name'] = user[0].proprietor_name
            request.session['branch_name'] = user[0].branch_name
            return redirect("/my-dashboard/")
        else:
            messages.error(request,'* Username and Password incorrect.')
            return redirect("/login/")

    return render(request, "showroom/branch_login.html", context)

def branch_logout(request):  
    request.session['id'] = False
    request.session['proprietor_name'] = False
    request.session['branch_name'] = False
    return redirect('/login/')

def add_selling_product(request):
    if not request.session['id']:
        return redirect('/login/')

    if request.method=="POST":
        product_id           = int(request.POST['product_name'])
        sell_quantity        = request.POST['sell_quantity']
        given_discount       = request.POST['given_discount']
        total_price          = request.POST['total_price']
        discription          = request.POST['discription']
        
        product = models.Product.objects.filter(id = product_id, status = True)
        if product and product[0].available_quantity > 0:
            models.SaleProducts.objects.create(
                salesman_id = int(request.session['salesman_id']),product_id = product_id, sale_quantity = sell_quantity,
                discount = given_discount, total_price = total_price, total_buy = product[0].buy_price * float(sell_quantity),  comment = comment)
            product.update(available_quantity = F('available_quantity') - sell_quantity)
            messages.success(request,"Product successfully added")
        else:
            messages.warning(request,'Product not available')    
        return redirect("/add-sales-product/")    

    if request.is_ajax():
        product = models.Product.objects.values().filter(id = int(request.GET.get('product_id')), status = True, available_quantity__gt = 0).first()
        if not product: product = "not_found"
        return JsonResponse(product, safe = False, content_type='application/json; charset=utf8')

    product_list      = models.ProductCat.objects.filter(status = True).order_by("category_name")
    customer_list     = models.CustomerRegistration.objects.all().order_by("name")
    context = {
        'product_list': product_list,         
        'customer_list': customer_list,         
    }
    return render(request,'showroom/branch/sale_products.html',context)

def load_category_product(request):
    product_list = models.Product.objects.filter(category_name_id = int(request.GET.get('category_id'))).order_by("product_name")

    return render(request, 'showroom/branch/load_product.html',{'product_list':product_list})

def customer_reg(request):

    return render(request, 'showroom/branch/customer_reg.html')
