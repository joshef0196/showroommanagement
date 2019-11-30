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
from showroom.utils import render_to_pdf
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

def branch_list(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    brance_list      = models.Branches.objects.all()
    context={
        'brance_list' : brance_list,
    }
    return render(request, "showroom/admin/branch_list.html", context)

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
            request.session['branch_logo'] = str(user[0].branch_logo)
            return redirect("/my-dashboard/")
        else:
            messages.error(request,'* Username and Password incorrect.')
            return redirect("/")

    return render(request, "showroom/branch_login.html", context)

def branch_logout(request):  
    request.session['id'] = False
    request.session['proprietor_name'] = False
    request.session['branch_name'] = False
    return redirect('/login/')

def cash_selling_product(request):
    if not request.session['id']:
        return redirect('/login/')

    if request.method=="POST":
        product_id           = int(request.POST['product_name'])
        customer_id          = int(request.POST['customer_id'])
        sale_quantity        = request.POST['sale_quantity']
        given_discount       = request.POST['given_discount']
        total_price          = request.POST['total_price']
        discription          = request.POST['discription']
        unit_price_cash      = request.POST['unit_price_cash']
        sale_date            = request.POST['sale_date']
        sale_date            = parse_date(str(sale_date))

        product = models.Product.objects.filter(id = product_id, status = True) 
        if product and product[0].available_quantity > 0:
            last_product = models.SaleProducts.objects.filter(branch_id = int(request.session['id'])).last()
            if last_product:last_invoice =  last_product.invoice + 1
            else: last_invoice =  1001

            models.SaleProducts.objects.create(
                invoice = last_invoice, branch_id = request.session['id'], customer_id = customer_id, product_id = product_id, sale_quantity = sale_quantity, sale_unit_price = unit_price_cash, 
                discount = given_discount, total_price = total_price, comment = discription, payment_type = "1", sale_date = sale_date)
            
            product.update(available_quantity = F('available_quantity') - sale_quantity)
            messages.success(request,"Product successfully added")
        else:
            messages.warning(request,'Product not available')    
        return redirect("/sold-product-list/")    

    if request.is_ajax():
        product = models.Product.objects.values().filter(id = int(request.GET.get('product_id')), status = True, available_quantity__gt = 0).first()
        if not product: product = "not_found"
        return JsonResponse(product, safe = False, content_type='application/json; charset=utf8')

    product_list      = models.Product.objects.raw("select * from showroom_product where branch_id = %s and status = true group by category_name_id",[int(request.session['id'])])
    customer_list     = models.CustomerRegistration.objects.filter(branch_id = int(request.session['id'])).order_by("name")
    context = {
        'product_list': product_list,         
        'customer_list': customer_list,         
    }
    return render(request,'showroom/branch/cash_sale_products.html',context)

def installment_selling_product(request):
    if not request.session['id']:
        return redirect('/login/')

    if request.method=="POST":
        product_id                = int(request.POST['product_name'])
        customer_id               = int(request.POST['customer_id'])
        sale_quantity             = request.POST['sale_quantity']
        given_discount            = request.POST['given_discount']
        total_price               = request.POST['total_price']
        due_amount                = request.POST['due_amount']
        cash_payment              = request.POST['cash_payment']
        next_installment_date     = request.POST['next_installment_date']
        discription               = request.POST['discription']
        unit_price_installment    = request.POST['unit_price_by_installment']
        next_installment_amount   = request.POST['next_installment_amount']
        sale_date                 = request.POST['sale_date']
        next_installment_date     = parse_date(str(next_installment_date))
        sale_date                 = parse_date(str(sale_date))

        
        product = models.Product.objects.filter(id = product_id, status = True) 
        if product and product[0].available_quantity > 0:
            last_product = models.SaleProducts.objects.filter(branch_id = int(request.session['id'])).last()
            if last_product:
                last_invoice =  last_product.invoice + 1
            else: 
                last_invoice =  1001
            last_installment = models.InstallmentCollection.objects.filter(branch_id = int(request.session['id'])).last()
            if last_installment:
                installment_invoice =  last_installment.invoice + 1
            else: 
                installment_invoice =  1001

            models.SaleProducts.objects.create(
                invoice = last_invoice, branch_id = request.session['id'], customer_id = customer_id, product_id = product_id, sale_quantity = sale_quantity, sale_unit_price = unit_price_installment, 
                discount = given_discount, total_price = total_price, comment = discription, payment_type = "2", due_amount = due_amount,
                next_installment_date = next_installment_date, next_installment_amount = next_installment_amount, sale_date = sale_date )
            
            product.update(available_quantity = F('available_quantity') - sale_quantity)
            models.InstallmentCollection.objects.create(invoice = installment_invoice, branch_id = request.session['id'], customer_id = customer_id, product_id = product_id,
                paid_amount = cash_payment, due_date = next_installment_date)
            messages.success(request,"Successfully submitted.")
        else:
            messages.warning(request,'Product not available')    
        return redirect("/sold-product-list/")    

    if request.is_ajax():
        product = models.Product.objects.values().filter(id = int(request.GET.get('product_id')), status = True, available_quantity__gt = 0).first()
        if not product: product = "not_found"
        return JsonResponse(product, safe = False, content_type='application/json; charset=utf8')

    product_list      = models.Product.objects.raw("select * from showroom_product where branch_id = %s and status = true group by category_name_id",[int(request.session['id'])])
    customer_list     = models.CustomerRegistration.objects.filter(branch_id = int(request.session['id']), status = True).order_by("name")
    context = {
        'product_list': product_list,         
        'customer_list': customer_list,         
    }
    return render(request,'showroom/branch/installment_sale_products.html',context)

def sold_product_list(request):
    if not request.session['id']:
        return redirect('/login/')

    if request.method=="POST":   
        product_list = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), payment_type = str(request.POST['payment_type']), status = True).order_by("-id")
        context = {
            'payment_type' : str(request.POST['payment_type']),
            'product_list' : product_list,
        }
        return render(request,"showroom/branch/sold_product_list.html",context)
    else:    
        product_list = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), status = True).order_by("-id")[:50]
        context = {
            'product_list' : product_list,
        }
        return render(request,"showroom/branch/sold_product_list.html",context)

def customer_product_list(request):
    if not request.session['id']:
        return redirect('/login/')
    area_list    = models.Area.objects.filter(branch_id = int(request.session['id']), status = True).order_by("-id")
    if request.is_ajax():
        search_by = (request.GET.get('search')).strip()
        product_list = models.SaleProducts.objects.values("product_id__category_name_id__category_name", "product_id__product_name","customer_id__name", "customer_id__mobile","sale_quantity","sale_unit_price","discount","total_price").filter(Q(customer_id__name__icontains = search_by)|Q(customer_id__email__icontains = search_by)|Q(customer_id__mobile__icontains = search_by)|Q(customer_id__mobile1__icontains = search_by)|Q(product_id__product_name__icontains = search_by), branch_id = int(request.session['id']), status = True).order_by("-id")
        if not product_list: product_list = "not_found"   
        return JsonResponse(list(product_list), safe = False, content_type='application/json; charset=utf8')

    elif request.method=="POST":   
        search_by = (request.POST['search']).strip()
        area_id   = int(request.POST['area_id'])

        if area_id == 0 and len(str(search_by)) > 0:
            product_list = models.SaleProducts.objects.filter(Q(customer_id__name__icontains = search_by)|Q(customer_id__email__icontains = search_by)|Q(customer_id__mobile__icontains = search_by)|Q(customer_id__mobile1__icontains = search_by)|Q(product_id__product_name__icontains = search_by), branch_id = int(request.session['id']), status = True).order_by("-id")
        # elif area_id != 0 and len(str(search_by)) > 0:
        #     product_list = models.SaleProducts.objects.filter((Q(customer_id__area_id = area_id) & Q(branch_id = int(request.session['id'])) & Q(status = True))|(Q(customer_id__name__icontains = search_by)|Q(customer_id__email__icontains = search_by)|Q(customer_id__mobile__icontains = search_by)|Q(customer_id__mobile1__icontains = search_by)|Q(product_id__product_name__icontains = search_by) & Q(branch_id = int(request.session['id'])) & Q(status = True))).order_by("-id")
        else:
            product_list = models.SaleProducts.objects.filter(customer_id__area_id = area_id, branch_id = int(request.session['id']), status = True).order_by("-id")
        context = {
            'product_list' : product_list,
            'search' : search_by,
            'area_list' : area_list,
            'area_id' : area_id,
        }
        return render(request,"showroom/branch/customer_product_list.html",context)
    else:    
        product_list = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), status = True).order_by("-id")[:50]
        context = {
            'product_list' : product_list,
            'area_list' : area_list,
        }
        return render(request,"showroom/branch/customer_product_list.html",context)

def installment_collection(request):
    if not request.session['id']:
        return redirect('/login/')

    if request.method=="POST":   
        search_by = (request.POST['search']).strip()
        product_list = models.SaleProducts.objects.filter(Q(customer_id__name__icontains = search_by)|Q(customer_id__email__icontains = search_by)|Q(customer_id__mobile__icontains = search_by)|Q(customer_id__mobile1__icontains = search_by)|Q(product_id__product_name__icontains = search_by), branch_id = int(request.session['id']), due_amount__gt = 0, payment_type = "2", status = True).order_by("-id")
        context = {
            'product_list' : product_list,
            'search' : search_by,
        }
        return render(request,"showroom/branch/installment_collection.html",context)
    else:    
        product_list = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), due_amount__gt = 0, payment_type = "2", status = True).order_by("next_installment_date")[:50]
        context = {
            'product_list' : product_list,
        }
        return render(request,"showroom/branch/installment_collection.html",context)

def installment_details(request, id):
    if not request.session['id']:
        return redirect('/login/')

    product = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), id = id)
    if request.method=="POST":   
        installment_amount = float(request.POST['installment_amount'])
        next_installment_date = parse_date(request.POST['next_installment_date'])
        collection_date = parse_date(request.POST['collection_date'])
        
        last_installment = models.InstallmentCollection.objects.filter(branch_id = int(request.session['id'])).last()
        if last_installment:
            installment_invoice =  last_installment.invoice + 1
        else: 
            installment_invoice =  1001
        if product and product[0].due_amount > 0:
            models.SaleProducts.objects.filter(branch_id = int(request.session['id']), id = id).update(due_amount = F("due_amount") - installment_amount, next_installment_amount = installment_amount, next_installment_date = next_installment_date)
            product = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), id = id)
            if product[0].due_amount <= 0:
                product.update(due_amount = 0, next_installment_date = None)
            models.InstallmentCollection.objects.create(invoice = installment_invoice, branch_id = request.session['id'], customer_id = product[0].customer_id, product_id = product[0].id,
                paid_amount = installment_amount, due_date = next_installment_date, payment_date = collection_date)
            return redirect("/installment-collection/") 

        elif product and product[0].due_amount <= 0:
            product.update(due_amount = 0, next_installment_date = None)
            return redirect(request.path) 
        else:
            return redirect("/installment-collection/")     
    else:    
        if product:
            context = {
                'product' : product[0],
            }
            return render(request,"showroom/branch/installment_details.html",context)
        else:
            return redirect("/installment-collection/")    

def installment_list(request):
    if not request.session['id']:
        return redirect('/login/')
    installment_list = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), payment_type = 2, status = True)
    context = {
        'installment_list' : installment_list,
    }
    return render(request, 'showroom/branch/installment_list.html', context)

def load_category_product(request):
    product_list = models.Product.objects.filter(branch_id = int(request.session['id']), category_name_id = int(request.GET.get('category_id')), available_quantity__gt = 0).order_by("product_name")

    return render(request, 'showroom/branch/load_product.html',{'product_list':product_list})

def load_product(request):
    product = models.Product.objects.values().filter(branch_id = int(request.session['id']), id = request.GET.get('product_id'), status = True).first()
    if not product: product = "not_found"
    return JsonResponse(product, safe = False, content_type='application/json; charset=utf8')

def customer_reg(request):
    if not request.session['id']:
        return redirect('/login/')

    brance = models.Branches.objects.filter(status = True)
    area_list = models.Area.objects.filter(status = True)
    context = {
        'brance' : brance,
        'area_list' : area_list,
    }
    if request.method=="POST":
        customer_name               = request.POST['customer_name']
        email                       = request.POST['email']
        mobile                      = request.POST['mobile']
        mobile1                     = request.POST['mobile1']
        nid_number                  = request.POST['nid_number']
        profession                  = request.POST['profession']
        reference_person            = request.POST['reference_person']
        reference_address           = request.POST['reference_address']
        reference_mobile            = request.POST['reference_mobile']
        present_address             = request.POST['present_address']
        permanent_address           = request.POST['permanent_address']
        area_id                     = int(request.POST['area_id'])

        order_file1 = ""
        if bool(request.FILES.get('customer_image', False)) == True:
            file = request.FILES['customer_image']
            order_file1 = "customer_image/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"customer_image/"):
                os.mkdir(settings.MEDIA_ROOT+"customer_image/")
            default_storage.save(settings.MEDIA_ROOT+"customer_image/"+file.name, ContentFile(file.read()))
        

        order_file2 = ""
        if bool(request.FILES.get('nid_image', False)) == True:
            file = request.FILES['nid_image']
            order_file2 = "nid_image/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"nid_image/"):
                os.mkdir(settings.MEDIA_ROOT+"nid_image/")
            default_storage.save(settings.MEDIA_ROOT+"nid_image/"+file.name, ContentFile(file.read()))
        
        if models.CustomerRegistration.objects.create(
            branch_id = request.session['id'], area_id = area_id, name = customer_name, email = email, mobile = mobile, mobile1 = mobile1, nid_number = nid_number, customer_image = order_file1, nid_image = order_file2, present_address = present_address,
            permanent_address = permanent_address, profession = profession, reference_person = reference_person, reference_address = reference_address, reference_mobile = reference_mobile
            ):
            messages.success(request,'Registration successfully!')
            return redirect("/customer-registration/")
        else:
            messages.error(request,"Please enter a valid value") 
            return redirect("/customer-registration/")

    return render(request, 'showroom/branch/customer_reg.html', context)

def edit_customer(request, id):
    if not request.session['id']:
        return redirect('/login/')

    brance        = models.Branches.objects.filter(status = True)
    area_list     = models.Area.objects.filter(status = True)
    edit_customer = models.CustomerRegistration.objects.filter(id = id, status = True).first()
    context = {
        'brance' : brance,
        'area_list' : area_list,
        'edit_customer' : edit_customer,
    }
    if request.method=="POST":
        customer_name               = request.POST['customer_name']
        email                       = request.POST['email']
        mobile                      = request.POST['mobile']
        mobile1                     = request.POST['mobile1']
        nid_number                  = request.POST['nid_number']
        profession                  = request.POST['profession']
        reference_person            = request.POST['reference_person']
        reference_address           = request.POST['reference_address']
        reference_mobile            = request.POST['reference_mobile']
        present_address             = request.POST['present_address']
        permanent_address           = request.POST['permanent_address']
        area_id                     = int(request.POST['area_id'])

        order_file1 = ""
        if bool(request.FILES.get('customer_image', False)) == True:
            file = request.FILES['customer_image']
            order_file1 = "customer_image/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"customer_image/"):
                os.mkdir(settings.MEDIA_ROOT+"customer_image/")
            default_storage.save(settings.MEDIA_ROOT+"customer_image/"+file.name, ContentFile(file.read()))
        

        order_file2 = ""
        if bool(request.FILES.get('nid_image', False)) == True:
            file = request.FILES['nid_image']
            order_file2 = "nid_image/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"nid_image/"):
                os.mkdir(settings.MEDIA_ROOT+"nid_image/")
            default_storage.save(settings.MEDIA_ROOT+"nid_image/"+file.name, ContentFile(file.read()))
        
        if models.CustomerRegistration.objects.filter(id = id).update(
            branch_id = request.session['id'], area_id = area_id, name = customer_name, email = email, mobile = mobile, mobile1 = mobile1, nid_number = nid_number, customer_image = order_file1, nid_image = order_file2, present_address = present_address,
            permanent_address = permanent_address, profession = profession, reference_person = reference_person, reference_address = reference_address, reference_mobile = reference_mobile
            ):
            messages.success(request,'Successfully updated.')
            return redirect("/customer-list/")
        else:
            messages.error(request,"Please enter a valid value") 
            return redirect("/customer-registration/")

    return render(request, 'showroom/branch/edit_customer.html', context)

def customer_list(request):
    if not request.session['id']:
        return redirect('/login/')
    customer_list = models.CustomerRegistration.objects.filter(branch_id = int(request.session['id']), status = True)
    context = {
        'customer_list' : customer_list,
    }
    return render(request, 'showroom/branch/customer_list.html', context)

def add_product_cat(request):
    if not request.session['id']:
        return redirect('/login/')
    brance_list      = models.Branches.objects.all()
    context={
        'brance_list' : brance_list,
    }
    if request.method=="POST":
        category_name   = request.POST['category_name']
        chack_cat = models.ProductCat.objects.filter(branch_id = int(request.session['id']), category_name = category_name)
        if not chack_cat:
            models.ProductCat.objects.create(branch_id = int(request.session['id']), category_name = category_name)
            messages.success(request,'Category setup successfully!')
            return redirect("/add-category/")
        else:
            messages.error(request,"Already added this name. ") 
            return redirect("/add-category/")

    return render(request,"showroom/branch/add_product_cat.html",context)

def add_area(request):
    if not request.session['id']:
        return redirect('/login/')
    if request.method=="POST":
        area_name   = request.POST['area_name']
        chack_cat = models.Area.objects.filter(area_name = area_name)
        if not chack_cat:
            models.Area.objects.create(branch_id = int(request.session['id']), area_name = area_name)
            messages.success(request,'Area setup successfully!')
            return redirect("/add-area/")
        else:
            messages.error(request,"Already added this name. ") 
            return redirect("/add-area/")

    return render(request,"showroom/branch/area_add.html")

def area_list(request):
    if not request.session['id']:
        return redirect('/login/')

    area_list      = models.Area.objects.filter(branch_id = int(request.session['id']), status = True)
    context={
        'area_list' : area_list,
    }
    return render(request, "showroom/branch/area_list.html", context)

def edit_area(request, id):
    if not request.session['id']:
        return redirect('/login/')

    edit_area        = models.Area.objects.filter(branch_id = int(request.session['id']), id = id).first()
    branch           = models.Branches.objects.filter(status = True).exclude(id = edit_area.branch_id)
    context={
        'edit_area' : edit_area,
        'branch' : branch,
    }
    if request.method=="POST":
        area_name   = request.POST['area_name']

        chack_cat = models.Area.objects.filter(branch_id = int(request.session['id']), area_name = area_name)
        if not chack_cat:
            models.Area.objects.filter(id = id).update(branch_id = int(request.session['id']), area_name = area_name)
            messages.success(request,'Successfully updated.')
            return redirect("/area-list/")
        else:
            messages.error(request,"Already added this name.")
            return redirect("/area-list/")

    return render(request,"showroom/branch/edit_area.html",context)

def edit_product_cat(request, id):
    if not request.session['id']:
        return redirect('/login/')
    edit_product_cat   = models.ProductCat.objects.filter(branch_id = int(request.session['id']), id = id).first()
    branch             = models.Branches.objects.filter(status = True).exclude(id = edit_product_cat.branch_id)
    context={
        'edit_product_cat' : edit_product_cat,
        'branch' : branch,
    }
    if request.method=="POST":
        category_name   = request.POST['category_name']

        chack_cat = models.ProductCat.objects.filter(branch_id = int(request.session['id']), category_name = category_name)
        if not chack_cat:
            models.ProductCat.objects.filter(id = id).update(branch_id = int(request.session['id']), category_name = category_name)
            messages.success(request,'Successfully updated.')
            return redirect("/category-list/")
        else:
            messages.error(request,"Already added this name.")
            return redirect("/category-list/")

    return render(request,"showroom/branch/edit_product_cat.html",context)

def delete_pro_category (request, id):
    if not request.session['id']:
        return redirect('/login/')

    models.ProductCat.objects.filter(branch_id = int(request.session['id']), id = id).delete()
    return redirect('/category-list/')

def category_list (request):
    if not request.session['id']:
        return redirect('/login/')

    cat_list      = models.ProductCat.objects.filter(branch_id = int(request.session['id']))
    context={
        'cat_list' : cat_list,
    }
    return render(request, "showroom/branch/cat_list.html", context)

def add_product(request):
    if not request.session['id']:
        return redirect('/login/')
    brance_list      = models.Branches.objects.all()
    pro_cat          = models.ProductCat.objects.filter(branch_id = int(request.session['id']))
    context={
        'brance_list' : brance_list,
        'pro_cat'     : pro_cat,
    }
    if request.method=="POST":
        category_name               = request.POST['category_name']
        product_name                = request.POST['product_name']
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
        
        if models.Product.objects.create(branch_id = int(request.session['id']), category_name_id = category_name, product_name = product_name, brand_name = request.session['id'],
                product_image = order_file1, product_model_number = product_model_number, product_color = product_color, total_quantity = total_quantity, available_quantity = total_quantity,
                unit_price_by_cash = unit_price_by_cash, unit_price_by_installment = unit_price_by_installment, buy_price = buy_price, maximum_discount = maximum_discount,
                total_price = total_price, discription = discription
            ):
            messages.success(request,'Product added successfully!')
            return redirect("/add-product/")
        else:
            messages.error(request,"Please enter a valid value.") 
            return redirect("/add-product/")

    return render(request,"showroom/branch/add_product.html",context)

def product_list(request):
    if not request.session['id']:
        return redirect('/login/')

    product_list      = models.Product.objects.filter(branch_id = int(request.session['id']), status = True)
    context={
        'product_list' : product_list,
    }
    return render(request, "showroom/branch/product_list.html", context)

def product_details(request, id):
    if not request.session['id']:
        return redirect('/login/')
    product      = models.Product.objects.filter(branch_id = int(request.session['id']), id = id).first()
    context={
        'product' : product,
    }
    return render(request, "showroom/branch/product_details.html", context)

def customer_details(request, id):
    if not request.session['id']:
        return redirect('/login/')
    customer_details      = models.CustomerRegistration.objects.filter(branch_id = int(request.session['id']), id = id).first()
    context={
        'customer_details' : customer_details,
    }
    return render(request, "showroom/branch/customer_details.html", context)

def unpaid_list(request):
    if not request.session['id']:
        return redirect('/login/')

    product_list   = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), due_amount__gt = 0)
    context={
        'product_list' : product_list,
    }
    return render(request, "showroom/branch/unpaid_list.html", context)

def dateover_due_list(request):
    if not request.session['id']:
        return redirect('/login/')

    product_list   = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), next_installment_date__lt = datetime.datetime.now().date(), due_amount__gt = 0)
    context={
        'product_list' : product_list,
    }
    return render(request, "showroom/branch/dateover_due_list.html", context)

def change_password(request):
    if not request.session['id']:
        return redirect('/login/')
    
    if request.method == "POST":
        current_pass = request.POST['current_pass']
        new_pass     = request.POST['new_pass']

        new_md5_obj = hashlib.md5(current_pass.encode())
        new_enc_pass = new_md5_obj.hexdigest()
        chk_user     = models.Branches.objects.filter(id = request.session['id'], password = new_enc_pass)
        if chk_user:
            new_md5_obj = hashlib.md5(new_pass.encode())
            new_enc_pass = new_md5_obj.hexdigest()
            models.Branches.objects.filter(id = request.session['id']).update(password = new_enc_pass)
            messages.success(request,'Your password has been changed.')
            return redirect("/change-password/")
        else:
            messages.error(request,'Invalid current Password.')
            return redirect("/change-password/")

    return render(request, "showroom/branch/change_password.html")

# ..............Report.............

# ..........For Branch...........
    
def daily_report(request):
    if not request.session['id']:
        return redirect('/login/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    daliy_report          = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), sale_date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), status = True)
    context={
        'company'      : company,
        'daliy_report' : daliy_report,
        'branch' : models.Branches.objects.filter(id = int(request.session['id']), status = True).first(),
        
    }

    pdf = render_to_pdf('showroom/branch/report/daily_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
def monthly_report(request):
    if not request.session['id']:
        return redirect('/login/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    monthly_report        = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), sale_date__month = datetime.datetime.now().month, status = True)
    context={
        'company'        : company,
        'monthly_report' : monthly_report,
        'branch' : models.Branches.objects.filter(id = int(request.session['id']), status = True).first(),
    }

    pdf = render_to_pdf('showroom/branch/report/monthly_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
def yearly_report(request):
    if not request.session['id']:
        return redirect('/login/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    yearly_report         = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), sale_date__year = datetime.datetime.now().year, status = True)
    context={
        'company'       : company,
        'yearly_report' : yearly_report,
        'branch' : models.Branches.objects.filter(id = int(request.session['id']), status = True).first(),
    }

    pdf = render_to_pdf('showroom/branch/report/yearly_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
def unpaid_report(request):
    if not request.session['id']:
        return redirect('/login/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    unpaid_report         = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), next_installment_date__gte = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), payment_type = "2", status = True)    
    context={
        'company'       : company,
        'unpaid_report' : unpaid_report,
        'branch' : models.Branches.objects.filter(id = int(request.session['id']), status = True).first(),
    }
    pdf = render_to_pdf('showroom/branch/report/unpaid_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
def dateover_due_report(request):
    if not request.session['id']:
        return redirect('/login/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    dateover_due_report   = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), next_installment_date__lt = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), payment_type = "2" , status = True)
    context={
        'company'       : company,
        'dateover_due_report' : dateover_due_report,
        'branch' : models.Branches.objects.filter(id = int(request.session['id']), status = True).first(),
    }

    pdf = render_to_pdf('showroom/branch/report/dateover_due_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def date_to_date_report(request):
    if not request.session['id']:
        return redirect('/login/')

    company  = models.CompanyInfo.objects.filter(status = True).first()
    if request.method == "POST":
        from_date = parse_date(request.POST['from_date'])
        to_date   = parse_date(request.POST['to_date'])

        date_to_date_sell  = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), sale_date__gte = from_date, sale_date__lte = to_date, status = True )
        context = {
            'company' : company,
            'from_date' : from_date,
            'to_date' : to_date,
            'date_to_date_sell' : date_to_date_sell,
            'branch' : models.Branches.objects.filter(id = int(request.session['id']), status = True).first(),
        }

        if date_to_date_sell:
            pdf = render_to_pdf('showroom/branch/report/date_wise_report.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:    
            return render(request,'showroom/branch/report/date_wise_form.html', context)

    return render(request,'showroom/branch/report/date_wise_form.html', {"company" : company})

# ...........For Admin............

def admin_daily_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    daliy_report          = models.SaleProducts.objects.filter(status = True)
    context={
        'company'      : company,
        'daliy_report' : daliy_report,
    }

    pdf = render_to_pdf('showroom/admin/report/daily_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
def admin_monthly_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    daliy_report          = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), status = True)
    context={
        'company'      : company,
        'daliy_report' : daliy_report,
    }

    pdf = render_to_pdf('showroom/admin/report/monthly_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    
def admin_yearly_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    company               = models.CompanyInfo.objects.filter(status = True).first()
    daliy_report          = models.SaleProducts.objects.filter(branch_id = int(request.session['id']), status = True)
    context={
        'company'      : company,
        'daliy_report' : daliy_report,
    }

    pdf = render_to_pdf('showroom/admin/report/yearly_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
