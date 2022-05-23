def get_route(request):
    return request.get_full_path().strip("/")
