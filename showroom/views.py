from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.db.models import F,Q
from django.db.models import Sum
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
import datetime
import hashlib, socket
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

def category_list (request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    cat_list      = models.ProductCat.objects.all()
    context={
        'cat_list' : cat_list,
    }
    return render(request, "showroom/admin/cat_list.html", context)

def add_brance(request):
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

def branch_list (request):
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