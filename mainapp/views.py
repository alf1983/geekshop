import json
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import ProductCategory, Product


def get_hot_product():
    products = Product.objects.filter(is_active=True, category__is_active=True)

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True, category__is_active=True)\
        .exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None, page=1):
    # print(pk)
    title = "каталог"

    basket = []
    total = 0
    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket_user = Basket().calc(request.user)
        for basket_user_raw in basket_user:
            _basket_item = {
                'item_name': basket_user_raw.product.name,
                'price_for_item': basket_user_raw.product.price,
                'quantity': basket_user_raw.quantity,
                'item_total_price': basket_user_raw.product.price * basket_user_raw.quantity
            }
            total += _basket_item['item_total_price']
            basket.append(_basket_item)
    links_menu_file = open("mainapp/templates/links_menu.json")
    links_menu = json.load(links_menu_file)
    links_menu_file.close()
    # [
    #     {'href': 'products_all', 'name': 'все'},
    #     {'href': 'products_home', 'name': 'дом'},
    #     {'href': 'products_office', 'name': 'офис'},
    #     {'href': 'products_modern', 'name': 'модерн'},
    #     {'href': 'products_classic', 'name': 'классика'},
    # ]
    all_categories = ProductCategory.objects.filter(is_active=True)
    hot_product = []
    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk, is_active=True)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)\
                .order_by('price')
    else:
        hot_product = get_hot_product()
        products = get_same_products(hot_product)
        category = {'name': 'горячие предложение'}
    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products_paginator,
        'all_categories': all_categories,
        'category': category,
        'basket': basket,
        'total': total,
        'hot_product': hot_product
    }
    return render(request, 'products.html', context=context)


def product(request, pk=None):
    # print(pk)
    links_menu_file = open("mainapp/templates/links_menu.json")
    links_menu = json.load(links_menu_file)
    links_menu_file.close()
    # [
    #     {'href': 'products_all', 'name': 'все'},
    #     {'href': 'products_home', 'name': 'дом'},
    #     {'href': 'products_office', 'name': 'офис'},
    #     {'href': 'products_modern', 'name': 'модерн'},
    #     {'href': 'products_classic', 'name': 'классика'},
    # ]
    all_categories = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        product = get_object_or_404(Product, pk=pk, is_active=True, category__is_active=True)
        # print(product.category)
    else:
        product = Product.objects.filter(is_active=True, category__is_active=True)[1]

    basket = []
    total = 0
    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket_user = Basket().calc(request.user)
        for basket_user_raw in basket_user:
            _basket_item = {
                'item_name': basket_user_raw.product.name,
                'price_for_item': basket_user_raw.product.price,
                'quantity': basket_user_raw.quantity,
                'item_total_price': basket_user_raw.product.price * basket_user_raw.quantity
            }
            total += _basket_item['item_total_price']
            basket.append(_basket_item)
    title = product.name
    category = ProductCategory.objects.get(pk=product.category_id)
    same_products = Product.objects.filter(category_id=category.pk, is_active=True, category__is_active=True)\
        .exclude(pk=product.pk).order_by('price')[:2]

    context = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
        'all_categories': all_categories,
        'category': category,
        'same_products': same_products,
        'basket': basket,
        'total': total
    }
    return render(request, 'product.html', context=context)
