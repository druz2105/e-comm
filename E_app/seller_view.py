import os
from E_Comm import settings as se
from .decoratos import authenticate_user, allowed_user
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import (Customer, OrderItem, Order, Address, Payment, Product_Detail, Shoes_Size, Shoes, Clothes,
                     Clothes_Size, Watches, Laptop, Mobile)
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, EditProfileForm
from django_q.tasks import async_task
import datetime
from django.contrib.auth.models import Group
from .seller_form import Product_Form, Laptop_Form, Watch_Form, Mobile_Form, Clothes_Form, Shoes_detail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import TemplateView, ListView, DetailView


def urlredirect(request):
    return redirect('/home/')


def register_seller(request):
    registered = False
    email_check = False
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email_id')
        password = request.POST.get('password_1')
        user_info = User(username=email, first_name=first_name, last_name=last_name, email=email)
        try:
            user_info.set_password(password)
            user_info.save()
            group = Group.objects.get(name='Seller')
            user_info.groups.add(group)
            user_info.save()
            registered = True
        except Exception as e:
            print(e)
            email_check = True
    return render(request, 'seller/registration.html', {'reg': registered, 'email': email_check})


@login_required
@allowed_user(allowed_roles=['Seller'])
def seller_home(request):
    return render(request, 'seller/seller_home.html')


@login_required
@allowed_user(allowed_roles=['Seller'])
def register_seller_product(request, pk):
    if pk == 'S':
        shoes = None
        form = Product_Form()
        form1 = Shoes_detail()
        if request.method == 'POST':
            form = Product_Form(request.POST, request.FILES)
            form1 = Shoes_detail(request.POST)
            if form1.is_valid():
                product_gender = form1.cleaned_data.get('product_gender')
                shoe_brand = form1.cleaned_data.get('shoe_brand')
                shoe_type = form1.cleaned_data.get('shoe_type')
                size = form1.cleaned_data.get('size')
                count = form1.cleaned_data.get('count')
                shoe_size = Shoes_Size(size=size, count=count)
                shoe_size.save()
                shoes = Shoes(product_gender=product_gender, shoe_brand=shoe_brand, shoe_type=shoe_type)
                shoes.save()
                shoes.shoes_size.add(shoe_size)
            if form.is_valid():
                image0 = form.cleaned_data.get('image0')
                image1 = form.cleaned_data.get('image1')
                image2 = form.cleaned_data.get('image2')
                product_name = form.cleaned_data.get('product_name')
                product_price = form.cleaned_data.get('product_price')
                product_color = form.cleaned_data.get('product_price')
                product_details = form.cleaned_data.get('product_details')
                product_discount = form.cleaned_data.get('product_discount')
                new_product = Product_Detail(image0=image0, image1=image1, image2=image2, product_name=product_name,
                                             product_price=product_price, product_color=product_color, product_type="S",
                                             product_details=product_details, discount=product_discount,
                                             shoes_detail=shoes)
                new_product.save()
        return render(request, 'seller/shoes_add.html', {'form': form, 'form1': form1})
    elif pk == 'L':
        laptop_detail_q = None
        form = Product_Form()
        form_l = Laptop_Form()
        if request.method == 'POST':
            form = Product_Form(request.POST, request.FILES)
            form_l = Laptop_Form(request.POST)
            if form_l.is_valid():
                count = form_l.cleaned_data.get('count')
                model_year = form_l.cleaned_data.get('model_year')
                model_name = form_l.cleaned_data.get('model_name')
                laptop_brand = form_l.cleaned_data.get('laptop_brand')
                screen_size = form_l.cleaned_data.get('screen_size')
                screen_type = form_l.cleaned_data.get('screen_type')
                weight = form_l.cleaned_data.get('weight')
                processor_brand = form_l.cleaned_data.get('processor_brand')
                processor_speed = form_l.cleaned_data.get('processor_speed')
                processor_type = form_l.cleaned_data.get('processor_type')
                resolution = form_l.cleaned_data.get('resolution')
                ram = form_l.cleaned_data.get('ram')
                storage_type = form_l.cleaned_data.get('storage_type')
                storage_size = form_l.cleaned_data.get('storage_size')
                hard_drive_interface = form_l.cleaned_data.get('hard_drive_interface')
                hard_drive_rotation_speed = form_l.cleaned_data.get('hard_drive_rotation_speed')
                operating_system = form_l.cleaned_data.get('operating_system')
                graphics_card_details = form_l.cleaned_data.get('graphics_card_details')
                graphics_card_ram_type = form_l.cleaned_data.get('graphics_card_ram_type')
                graphics_card_interface = form_l.cleaned_data.get('graphics_card_interface')
                graphics_coprocessor = form_l.cleaned_data.get('graphics_coprocessor')
                battery_details = form_l.cleaned_data.get('battery_details')
                max_memory_supported = form_l.cleaned_data.get('max_memory_supported')
                usb_ports = form_l.cleaned_data.get('usb_ports')
                optical_drive_type = form_l.cleaned_data.get('optical_drive_type')
                hardware_interface = form_l.cleaned_data.get('hardware_interface')
                manufacturer = form_l.cleaned_data.get('manufacturer')
                connector_type = form_l.cleaned_data.get('connector_type')
                power_source = form_l.cleaned_data.get('power_source')
                laptop_detail_q = Laptop(count=count, model_name=model_name, model_year=model_year,
                                         laptop_brand=laptop_brand, screen_size=screen_size, screen_type=screen_type,
                                         weight=weight, processor_type=processor_type, processor_brand=processor_brand,
                                         processor_speed=processor_speed, resolution=resolution, ram=ram,
                                         storage_size=storage_size, storage_type=storage_type,
                                         hard_drive_interface=hard_drive_interface,
                                         hard_drive_rotation_speed=hard_drive_rotation_speed,
                                         operating_system=operating_system, graphics_card_details=graphics_card_details,
                                         graphics_card_ram_type=graphics_card_ram_type,
                                         graphics_card_interface=graphics_card_interface,
                                         graphics_coprocessor=graphics_coprocessor, battery_details=battery_details,
                                         max_memory_supported=max_memory_supported, usb_ports=usb_ports,
                                         optical_drive_type=optical_drive_type, hardware_interface=hardware_interface,
                                         manufacturer=manufacturer, connector_type=connector_type,
                                         power_source=power_source)
                laptop_detail_q.save()
                print(laptop_detail_q)
            if form.is_valid():
                image0 = form.cleaned_data.get('image0')
                image1 = form.cleaned_data.get('image1')
                image2 = form.cleaned_data.get('image2')
                product_name = form.cleaned_data.get('product_name')
                product_price = form.cleaned_data.get('product_price')
                product_color = form.cleaned_data.get('product_price')
                product_details = form.cleaned_data.get('product_details')
                product_discount = form.cleaned_data.get('product_discount')
                new_product = Product_Detail(image0=image0, image1=image1, image2=image2, product_name=product_name,
                                             product_price=product_price, product_color=product_color, product_type="S",
                                             product_details=product_details, discount=product_discount,
                                             shoes_detail=laptop_detail_q)
                new_product.save()
        return render(request, 'seller/laptop_add.html', {'form': form, 'form_l': form_l})
    elif pk == 'C':
        print('Customer')
    elif pk == 'W':
        print('Watch')
    elif pk == 'M':
        print('Mobile')
    return render(request, 'seller/registration.html')
