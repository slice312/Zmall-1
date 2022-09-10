import random

from django.contrib.auth import authenticate

from rest_framework.exceptions import AuthenticationFailed

from decouple import config

from user.models import CustomUser as User


def register_social_user(provider, email):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=config('SOCIAL_SECRET'))

            return {
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'email': email,
            'password': config('SOCIAL_SECRET')}

        user = User.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=config('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'tokens': new_user.tokens()
        }
