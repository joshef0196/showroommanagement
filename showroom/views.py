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
            messages.error(request,'* Please Enter Valid Value.')
            return redirect("/")

    return render(request, "showroom/login.html")

def logout(request):  
    request.session['user'] = False
    request.session['usertype'] = False
    return redirect('/')