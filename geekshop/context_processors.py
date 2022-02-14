from django.http import HttpResponse


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
