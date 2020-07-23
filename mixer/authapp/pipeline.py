import urllib
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from mixer.settings import MEDIA_ROOT


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name == "google-oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'picture' in response.keys():
            picture = requests.get(response['picture']).content
            file_name = f'users_avatar/{user.username}_logo.jpg'
            with open(f'{MEDIA_ROOT}/{file_name}', 'wb') as f:
                f.write(picture)
            user.avatar = file_name

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
        if 'photo' in response.keys():
            picture = requests.get(response['photo']).content
            file_name = f'users_avatar/{user.username}_logo.jpg'
            with open(f'{MEDIA_ROOT}/{file_name}', 'wb') as f:
                f.write(picture)
            user.avatar = file_name
        # if 'photo' in response.keys():
        #     id_user = response.get('id')
        #     urllib.request.urlretrieve(
        #         response.get('photo'),
        #         f'media/users_avatar/{id_user}' + '.jpg')
        #     user.avatar = f'media/users_avatar/{id_user}' + '.jpg'
        user.save()
