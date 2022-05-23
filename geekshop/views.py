from django.shortcuts import render
from mainapp.models import Product


def index(request):
    title = "магазин"
    products = Product.objects.all()[:2]
    context = {
        'title': title,
        'products': products
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    title = "наши контакты"
    context = {
        'title': title,
        "current_route": "contacts"
    }
    return render(request, 'contact.html', context=context)
