import json

from django.shortcuts import render


def products(request):
    title = "каталог"
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
    context = {
        'title': title,
        'links_menu': links_menu
    }
    return render(request, 'products.html', context=context)

