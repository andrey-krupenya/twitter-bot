from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from app_for_trafic.models import Users, RoleUserTwitter
from bot_for_trafic.base_conf import BaseConf


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token_from_request = request.META.get('HTTP_X_AUTH_TOKEN') or request.query_params.get('HTTP_X_AUTH_TOKEN')
        if BaseConf.AUTH_TOKEN_SERVICE != token_from_request:
            raise exceptions.AuthenticationFailed(_('No such token'))

        return True, True


class CustomSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):

        session_keys = list(request.session.keys())

        if 'userid' in session_keys or 'id' in session_keys:

            id_user = request.session.get("id") or request.session.get("userid")

            try:
                user = Users.objects.get(id=id_user, id_role_id=RoleUserTwitter.ADMIN)
            except Users.DoesNotExist:
                raise exceptions.AuthenticationFailed(_('No such user'))

            return user, True
        raise exceptions.AuthenticationFailed(_('No such user'))
