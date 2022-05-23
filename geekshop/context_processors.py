from django.http import HttpResponse

from basketapp.models import Basket


def get_route(request):
    route = request.get_full_path().split("/")
    if not route[1]:
        route[1] = 'home'
        route.append("")
    return {
        "route": route[1],
        "route_admin": route[2]
    }


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ajax_test(request):
    if is_ajax(request=request):
        return True
    return False


def get_basket(request):
    basket = []
    total = 0
    total_quantity = 0
    if request.user.is_authenticated:
        basket_user = Basket().calc(request.user)
        for basket_user_raw in basket_user:
            _basket_item = {
                'item_name': basket_user_raw.product.name,
                'price_for_item': basket_user_raw.product.price,
                'quantity': basket_user_raw.quantity,
                'item_total_price': basket_user_raw.product.price * basket_user_raw.quantity
            }
            total_quantity += basket_user_raw.quantity
            total += _basket_item['item_total_price']
            basket.append(_basket_item)
    return {"basket": basket, "total": total, "basket_total_quantity": total_quantity}
