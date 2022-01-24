def get_route(request):
    route = request.get_full_path().split("/")[1]
    if not route:
        route = 'home'
    return {
        "route": route
    }
