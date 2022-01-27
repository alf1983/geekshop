from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    title = "магазин"
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
    products = Product.objects.all()[:2]
    context = {
        'title': title,
        'products': products,
        'basket': basket,
        'total': total
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    title = "наши контакты"

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
    context = {
        'title': title,
        "current_route": "contacts",
        'basket': basket,
        'total': total
    }
    return render(request, 'contact.html', context=context)
