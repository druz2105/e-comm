import os
from E_Comm import settings as se
from .decoratos import authenticate_user, allowed_user
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import Customer, Address, Product_Detail, Order, OrderItem, Payment
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, EditProfileForm
from django_q.tasks import async_task
import datetime
from django.contrib.auth.models import Group
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import TemplateView, ListView, DetailView


def urlredirect(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'Customer' or group == 'Admin':
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/seller_home/')


@authenticate_user
def register(request):
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
            group = Group.objects.get(name='Customer')
            user_info.groups.add(group)
            user_info.save()
            registered = True
        except Exception as e:
            print(e)
            email_check = True
    return render(request, 'customer/registration.html', {'reg': registered, 'email': email_check})


@authenticate_user
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                if group == 'Customer' or group == 'Admin':
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponseRedirect('/seller_home/')
            else:
                return HttpResponse("You are not active user")
        else:
            return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/login.html')


@login_required
def edit_profile(request):
    form = EditProfileForm()
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            mobile_no = form.cleaned_data.get('mobile_no')
            alternate_mobile_number = form.cleaned_data.get('alternate_mobile_number')
            apartment_address = form.cleaned_data.get('apartment_address')
            street_address = form.cleaned_data.get('street_address')
            country = form.cleaned_data.get('country')
            state = form.cleaned_data.get('state')
            zip = form.cleaned_data.get('zip')
            address = Address(user_id=request.user, apartment_address=apartment_address, street_address=street_address,
                              country=country,
                              state=state, zip=zip, default=True, address_type='B')
            address.save()
            model = Customer(user_id=request.user, mobile_no=mobile_no, alternate_mobile_number=alternate_mobile_number)
            model.save()
            model.addresses.add(address)
            return HttpResponseRedirect('/home/')
        else:
            form = EditProfileForm()

    return render(request, 'customer/edit_profile.html', {'form': form})


@login_required
@allowed_user(allowed_roles=['Customer', 'Admin'])
def Home(request):
    today = datetime.datetime.today()
    week_ago = today - datetime.timedelta(days=15)
    product = Product_Detail.objects.all().filter(
        added_date__range=[week_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')])
    Product_Detail.objects.all().filter(product_deal_week=True).update(discount=25)
    Product_Detail.objects.all().filter(product_deal_month=True).update(discount=15)
    deal_week = Product_Detail.objects.all().filter(product_deal_week=True)
    deal_month = Product_Detail.objects.all().filter(product_deal_month=True)
    product_w_o_deal = Product_Detail.objects.all()
    context = {'product': product, 'deal_week': deal_week, 'deal_month': deal_month}
    for k in product_w_o_deal:
        print(k)
        k.deal_price = k.product_price - k.product_price * k.discount / 100
        k.save()
        k.deal_price = 0
    return render(request, 'customer/home.html', context)


@login_required
def product_short_view(request, pk):
    print(pk)
    short_product_type = Product_Detail.objects.filter(product_type=pk)
    if len(short_product_type) == 0:
        return redirect('/home/')
    else:
        return render(request, 'customer/product_short.html', {'product': short_product_type})


@login_required
def details_product(request, pk):
    Item = get_object_or_404(Product_Detail, id=pk)
    product_detail = Product_Detail.objects.filter(product_name=Item)
    if product_detail[0].product_type == 'S':
        if product_detail[0].shoes_detail.shoes_size.exists():
            return render(request, 'customer/shoes-product.html', {'objects': product_detail})
        else:
            return HttpResponse('Currently Out of Stock')
    elif product_detail[0].product_type == 'L':
        return render(request, 'customer/laptop-product.html', {'objects': product_detail})
    elif product_detail[0].product_type == 'M':
        return render(request, 'customer/mobile-product.html', {'objects': product_detail})
    elif product_detail[0].product_type == 'C':
        return render(request, 'customer/clothes-product.html', {'objects': product_detail})
    elif product_detail[0].product_type == 'W':
        return render(request, 'customer/watch-product.html', {'objects': product_detail})


def post_email(request):
    if request.method == 'POST':
        subject = 'LINK TO REGISTER AS NEW SELLER'
        html_message = render_to_string('link_template.html')
        plain_message = strip_tags(html_message)
        from_email = 'druz2105@gmail.com'
        to = request.POST.get('EMAIL')
        message = Mail(
            from_email=from_email,
            to_emails=to,
            subject=subject,
            plain_text_content=plain_message,
        )
        sg = SendGridAPIClient(se.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return redirect('/home/')
    return render(request, 'customer/form_html.html')


@login_required
def add_cart(request, pk):
    if request.method == 'POST':
        try:
            Item = get_object_or_404(Product_Detail, id=pk)
            size = request.POST.get('size')
            oi, create = OrderItem.objects.get_or_create(user=request.user, item=Item, order_size=size,
                                                         ordered=False)
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(item__product_name=Item.product_name, order_size=size).exists():
                    oi.product_quantity += 1
                    oi.save()
                else:
                    order.items.add(oi)
            else:
                order = Order.objects.create(user=request.user, order_id=oi.order_id, order_date=timezone.now())
                order.items.add(oi)
            return redirect('/home/')
        except:
            return redirect('/home/')


@allowed_user(allowed_roles=['Seller', 'admin'])
def add_product(request):
    return render(request, 'customer/add_product.html')


@login_required
def update_cart(request, pk):
    oi, create = OrderItem.objects.get_or_create(user=request.user, order_id=pk,
                                                 ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(order_id=pk).exists():
            oi.product_quantity += 1
            oi.save()

    return redirect('/cart/')


@login_required
def remove_item_cart(request, pk):
    oi, create = OrderItem.objects.get_or_create(user=request.user, order_id=pk,
                                                 ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(order_id=pk).exists():
            oi.product_quantity -= 1
            oi.save()

    return redirect('/cart/')


@login_required
def remove_cart(request, pk):
    order_qs = Order.objects.filter(user=request.user, order_id=pk, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(order_id=pk).exists():
            oi = OrderItem.objects.filter(user=request.user, order_id=pk, ordered=False)[0]
            order.items.remove(oi)
            oi.product_quantity = 1
            oi.save()
            return redirect('/cart/')
        else:
            return redirect('/cart/')
    else:
        return redirect('/cart/')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(user_login))


@login_required
def cart(request):
    try:
        order_qs = Order.objects.get(user=request.user, ordered=False)
        return render(request, 'customer/cart.html', {'order': order_qs})
    except ObjectDoesNotExist:
        messages.error(request, "You do not have active order")
        return redirect('/home/')


@login_required
def checkout(request):
    try:
        order_qs = Order.objects.get(user=request.user, ordered=False)
        print(order_qs.order_id)
        form = CheckoutForm()
        context = {'order': order_qs, 'form': form}
        use_default = Address.objects.filter(user_id=request.user, default=True, address_type='B')
        if use_default:
            context['default_address'] = use_default[0]

        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                apartment_address = form.cleaned_data.get('apartment_address')
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                same_shipping = form.cleaned_data.get('same_shipping')
                payment_option = form.cleaned_data.get('payment_option')
                model = Address(user_id=request.user, apartment_address=apartment_address,
                                street_address=street_address, state=state, zip=zip,
                                country=country,
                                address_type='B')
                model.save()
                order_qs.billing_address = model
                order_qs.ordered = True
                order_qs.save()
                if same_shipping:
                    model_ship = Address(user_id=request.user, apartment_address=apartment_address,
                                         street_address=street_address, state=state, zip=zip,
                                         country=country,
                                         address_type='S')
                    model_ship.save()
                    order_qs.shipping_address = model_ship
                    order_qs.save()
                    if payment_option == 'C':
                        return redirect("/payment/COD/%s/" % order_qs.order_id)
                    else:
                        pass
                else:
                    s_apartment_address = request.POST.get('shipping_apartment_address')
                    s_street_address = request.POST.get('shipping_street_address')
                    s_country = request.POST.get('shipping_country')
                    s_state = request.POST.get('shipping_state')
                    s_zip = request.POST.get('shipping_zip')
                    if s_apartment_address == '' or s_street_address == '' or s_state == '' or s_zip == '':
                        return redirect('#/')
                    else:
                        model_new_ship = Address(user_id=request.user, apartment_address=s_apartment_address,
                                                 street_address=s_street_address, state=s_state, zip=s_zip,
                                                 country=s_country,
                                                 address_type='S')
                        model_new_ship.save()
                        order_qs.shipping_address = model_new_ship
                        order_qs.save()
                        if payment_option == 'C':
                            return redirect("/payment/COD/%s/" % order_qs.order_id)
                        else:
                            pass
            else:
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_shipping = form.cleaned_data.get('same_shipping')
                payment_option = form.cleaned_data.get('payment_option')
                if use_default_billing and same_shipping:
                    add_default = Address.objects.filter(user_id=request.user, default=True)
                    if add_default.exists():
                        address = add_default[0]
                        order_qs.billing_address = address
                        order_qs.shipping_address = address
                        order_qs.ordered = True
                        order_qs.save()
                        if payment_option == 'C':
                            return redirect("/payment/COD/%s/" % order_qs.order_id)
                        else:
                            pass
                s_apartment_address = request.POST.get('shipping_apartment_address')
                s_street_address = request.POST.get('shipping_street_address')
                s_country = request.POST.get('shipping_country')
                s_state = request.POST.get('shipping_state')
                s_zip = request.POST.get('shipping_zip')
                if s_apartment_address == '' or s_street_address == '' or s_state == '' or s_zip == '':
                    return redirect('#/')
                else:
                    model_new_ship = Address(user_id=request.user, apartment_address=s_apartment_address,
                                             street_address=s_street_address, state=s_state, zip=s_zip,
                                             country=s_country,
                                             address_type='S')
                    model_new_ship.save()
                    order_qs.shipping_address = model_new_ship
                    order_qs.ordered = True
                    order_qs.save()
                    if payment_option == 'C':
                        return redirect("/payment/COD/%s/" % order_qs.order_id)
                    else:
                        pass
        return render(request, 'customer/checkout.html', context)
    except ObjectDoesNotExist:
        return redirect('/home/')


@login_required
def payment(request, pk, id):
    try:
        order_qs = Order.objects.get(user=request.user, order_id=id)
        payment_mod = Payment(user=request.user, payment_method=pk, amount=float(order_qs.get_total()))
        payment_mod.save()
        order_qs.payment = payment_mod
        order_qs.order_date = payment_mod.timestamp
        order_qs.save()
        id = order_qs.order_id
        order_get = Order.objects.filter(user=request.user, order_id=id)
        try:
            async_task('E_app.task.confirm_order', request.user, request.user.email, id)
            return render(request, 'customer/confirmation.html', {'order': order_get, 'object': order_qs})
        except Exception as e:
            order_qs = Order.objects.get(user=request.user, order_id=id)
            order_qs.canceled = True
            order_qs.save()
            print(e)
        return render(request, 'customer/confirmation.html', {'order': order_get, 'object': order_qs})
    except ObjectDoesNotExist:
        return redirect('/home/')


def Contact(request):
    return render(request, 'customer/contact.html')
