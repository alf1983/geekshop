from django.http import HttpResponse


def get_route(request):
    route = request.get_full_path().split("/")[1]
    if not route:
        route = 'home'
    return {
        "route": route
    }


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ajax_test(request):
    if is_ajax(request=request):
        return True
    return False
