import requests
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from mixer.settings import MEDIA_ROOT


def save_user_profile(backend, user, response, *args, **kwargs):
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
            min_age = response['ageRange']['min']
            if int(min_age) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()

    elif backend.name == 'vk-oauth2':
        if 'photo' in response.keys():
            picture = requests.get(response['photo']).content
            file_name = f'users_avatar/{user.username}_logo.jpg'
            with open(f'{MEDIA_ROOT}/{file_name}', 'wb') as f:
                f.write(picture)
            user.avatar = file_name
        user.save()
