from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse

from basketapp.models import Basket


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))
    form_errors = ""
    if request.method == 'POST':
        form_errors = login_form.errors
    content = {
        'title': title,
        'login_form': login_form,
        'errors': form_errors,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    form_errors = ""
    # print(request.method)
    if request.method == 'POST':
        form_errors = register_form.errors
    content = {
        'title': title,
        'register_form': register_form,
        'errors': form_errors
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'
    basket = []
    total = 0
    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket_user = Basket.calc(request.user)
        for basket_user_raw in basket_user:
            _basket_item = {
                'item_name': basket_user_raw.product.name,
                'price_for_item': basket_user_raw.product.price,
                'quantity': basket_user_raw.quantity,
                'item_total_price': basket_user_raw.product.price * basket_user_raw.quantity
            }
            total += _basket_item['item_total_price']
            basket.append(_basket_item)
    form_errors = ""
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
        else:
            form_errors = edit_form.errors
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
        'errors': form_errors,
        'basket': basket,
        'total': total
    }

    return render(request, 'authapp/edit.html', content)
