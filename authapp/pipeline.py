from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.forms import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, **kwargs):
    # print(user.email + 'hello')
    if backend.name != 'facebook':
        return
    fb_link = 'https://www.facebook.com/profile.php?id=' + response['id']
    user.shopuserprofile.social_link = fb_link
    user.shopuserprofile.save()
    api_url = urlunparse((
        'https',
        'graph.facebook.com',
        'v4.0/' + response['id'],
        None,
        urlencode(
            OrderedDict(
                fields=','.join(['email', 'birthday', 'gender', 'link']),
                access_token=response['access_token'],
            ),
        ),
        None,
    ))
    print(api_url)
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    print(resp.json())
    data = resp.json()
    if data['birthday']:
        # print(data)
        birthday_object = datetime.strptime(data['birthday'], '%m/%d/%Y')
        try:
            birthday = birthday_object.replace(year=datetime.today().year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = birthday_object.replace(year=datetime.today().year, month=birthday_object.month + 1, day=1)
        if birthday > datetime.today():
            age = datetime.today().year - birthday_object.year - 1  # - 17 для теста
        else:
            age = datetime.today().year - birthday_object.year  # - 17 для теста
        # print(age)
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.facebook.FacebookOAuth2')
        else:
            user.age = age
            user.shopuserprofile.save()
    if data['email']:
        # print(len(user.email))
        # print(data['email'])
        if len(user.email) == 0:
            user.email = data['email']
            print(user.email)
            user.shopuserprofile.save()
    if data['gender']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['gender'] == 'male' else ShopUserProfile.FEMALE

