from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from geekshop.context_processors import ajax_test
from mainapp.models import Product


@login_required
def basket(request):
    title = 'корзина'
    total = 0
    basket_items = []
    basket_items_ordered = Basket.calc(request.user)
    for basket_item in basket_items_ordered:
        _basket_item = {
                    'basket_pk': basket_item.pk,
                    'item_name': basket_item.product.name,
                    'item_img': basket_item.product.image,
                    'price_for_item': basket_item.product.price,
                    'quantity': basket_item.quantity,
                    'item_total_price': basket_item.product.price * basket_item.quantity
                }
        total += _basket_item['item_total_price']
        basket_items.append(_basket_item)

    content = {
        'title': title,
        'basket_items': basket_items,
        'total': total,
        'basket': basket_items
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    content = {}
    return render(request, 'basketapp/order_form.html', content)


@login_required
def basket_edit(request, pk, quantity):
    if ajax_test(request):
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        total = 0
        basket_items = []
        basket_items_ordered = Basket.calc(request.user)
        for basket_item in basket_items_ordered:
            _basket_item = {
                'basket_pk': basket_item.pk,
                'item_name': basket_item.product.name,
                'item_img': basket_item.product.image,
                'price_for_item': basket_item.product.price,
                'quantity': basket_item.quantity,
                'item_total_price': basket_item.product.price * basket_item.quantity
            }
            total += _basket_item['item_total_price']
            basket_items.append(_basket_item)

        content = {
            'basket_items': basket_items,
            'total': total
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
