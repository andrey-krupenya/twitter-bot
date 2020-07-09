#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class BaseConf(object):

    def __int__(self):
        pass

    DATABASES_MAIN = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'USER': 'root',
            'PASSWORD': '123456456',
            'NAME': 'bot_db',
            'OPTIONS': {
                "init_command": "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;"
            },
        }
    }

    telegram_chat_id = os.getenv('telegram_chat_id', -123123123)
    telegram_token = os.getenv('telegram_token', 'bot12123:AAdf1pMO_TuoGrdfvrfvvf83eWPpl555C1AxM')

    email_host = os.getenv('email_host', 'mail.org')
    email_host_password = os.getenv('email_host_password', 'pass_to_smtp')
    email_host_user = os.getenv('email_host_user', 'user_to_access')
    email_port = os.getenv('email_port', 465)
    SITE_URL_BASE = os.getenv('site_url', 'social-bot.domain')
    MAIN_SITE_URL = ['localhost',
                     SITE_URL_BASE]

    BASE_TEXT_FOR_SEARCH = "candy"

    DEBUG_MAIN = False

    # REDIS
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB_LETTER = 5
    REDIS_PREFIX_LETTER = "tweet_"

    # CELERY
    CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 60 * 60 * 24 * 4}  # 4 days
    CELERY_IMPORTS = ('app_for_trafic.tasks',)
    CELERY_BROKER_URL = 'amqp://localhost'
    CELERY_RESULT_BACKEND = 'rpc'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    CELERY_TASK_RESULT_EXPIRES = 12 * 60 * 60
    CELERYD_HIJACK_ROOT_LOGGER = False
    CELERY_BEAT_SCHEDULE = {
        'get_tweets_for_reply': {
            'task': 'tasks.search_tweet_by_text',
            'schedule': 60 * 10,  # 10 minutes
            'options': {'queue': 'received_queue'},
            'args': ([90, BASE_TEXT_FOR_SEARCH])
        },
    }
