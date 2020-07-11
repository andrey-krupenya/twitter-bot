import logging
import os
import random

from unittest import TestCase
from django.test import Client
from rest_framework import status

from app_for_trafic.factories_model_test import (
    UsersFactory,
    TweetsFactory,
    UserTwitterFactory)
from app_for_trafic import models
from bot_for_trafic import settings_test
from bot_for_trafic.base_conf import BaseConf

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


class TweetAPITest(TestCase):
    fixtures = [settings_test.FIXTURE_FILES, ]
    test_email = 'test_case@test.com'

    @classmethod
    def setUpTestData(cls):
        if not os.path.exists(settings_test.FIXTURE_FILES):
            logger.info('[i] Please check fixture existing')

        UsersFactory.create_batch(3)

        for _ in range(10):
            TweetsFactory.create(
                status=models.StatusTweet.objects.get(pk=(_ % 2 + 1))
            )

        for _ in range(10):
            UserTwitterFactory.create(
                id_role=models.RoleUserTwitter.objects.get(pk=(_ % 2 + 1)),
                id_status=models.StatusTweet.objects.get(pk=(_ % 2 + 1))
            )

    def setUp(self):
        self.client = Client(HTTP_X_AUTH_TOKEN=BaseConf.AUTH_TOKEN_SERVICE)

        session = self.client.session
        session['userid'] = models.Users.objects.all().first().id
        session.save()

    def test_credential_for_access_200(self):
        data = models.UserTwitter.objects.all().only('id')
        for item in data:

            response = self.client.get(f'check_user/{item.id}')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(response.content, dict())

    def test_credential_for_access_404(self):
        id_not_exists_user = 0
        response = self.client.get(f'check_user/{id_not_exists_user}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, {"message": f"Wrong user ID: {id_not_exists_user}"})

    def test_search_by_query_string_200(self):
        data = models.UserTwitter.objects.all().only('id')
        for item in data:
            response = self.client.get(f'search_text/{item.id}/searchTextInTweets=test')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(response.content, dict())

    def test_search_by_query_string_422(self):
        id_not_exists_user = 0
        response = self.client.get(f'search_text/{id_not_exists_user}/searchTextInTweets1=test')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json['status'], 'failed')

    def test_search_by_query_string_404(self):
        id_not_exists_user = 0
        response = self.client.get(f'search_text/{id_not_exists_user}/searchTextInTweets=test')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"message": f"Wrong user ID: {id_not_exists_user}"})

    def test_reply_on_tweet_200(self):
        tweet_id = random.randint(100000, 1000000000)
        response = self.client.get(f'send_test_reply/{tweet_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json(), {"message": f"Work do!"})

    def test_reply_on_tweet_404(self):
        id_not_exists_user = 0
        models.UserTwitter.objects.filter(
            id_role=models.RoleUserTwitter.USER
        ).update(
            {'id_role': models.RoleUserTwitter.ADMIN}
        )

        response = self.client.get(f'send_test_reply/{id_not_exists_user}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"message": f"Can't get auth"})
