from rest_framework.authentication import TokenAuthentication


class CustomBearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'