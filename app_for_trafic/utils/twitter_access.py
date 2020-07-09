from app_for_trafic.models import UserTwitter, RoleUserTwitter, StatusUserTwitter


class TwitterAccess(object):
    def __init__(self, id_role: int):
        data_auth = self.get_auth_data(id_role)
        self.consumer_key_ = data_auth.get('consumer_key')
        self.consumer_secret_ = data_auth.get('consumer_secret')
        self.access_token_ = data_auth.get('access_token')
        self.access_token_secret_ = data_auth.get('access_token_secret')
        self.dict_count_use = {"count_use": int(data_auth.get('count_use')) + 1}
        self.id_record = data_auth.get('id')

    @staticmethod
    def get_auth_data(role: int):
        return UserTwitter.objects.filter(
            id_role=role,
            id_status=StatusUserTwitter.ENABLE
        ).order_by(
            'count_use'
        ).values(
            'name', 'consumer_key',
            'consumer_secret',
            'access_token',
            'access_token_secret',
            'id_role__name',
            'id_status__status',
            'count_use', 'id'
        ).first()

    @property
    def get_consumer_key(self):
        return self.consumer_key_

    @property
    def get_consumer_secret(self):
        return self.consumer_secret_

    @property
    def get_access_token(self):
        return self.access_token_

    @property
    def get_access_token_secret(self):
        return self.access_token_secret_

    @property
    def get_count_use(self):
        return self.dict_count_use

    @property
    def get_id(self):
        return self.id_record
