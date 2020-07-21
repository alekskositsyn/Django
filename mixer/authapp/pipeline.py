from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name == "google-oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        # raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()

    elif backend.name == 'vk-oauth2':
        api_url = urlunparse(
            ('https',
             'api.vk.com',
             '/method/users.get',
             None,
             urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                   access_token=response['access_token'],
                                   v='5.120')),
             None
             )
        )

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data.get('sex'):
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data.get('about'):
            user.shopuserprofile.aboutMe = data['about']

        if data.get('bdate'):
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year

            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age

        if backend.name == 'vk-oauth2':
            url = response.get('photo_100', '')

        if url:
            user.avatar = url
            user.save()

        user.save()
