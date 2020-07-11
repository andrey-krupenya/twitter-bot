#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery.utils.log import get_task_logger
from django.db.models import Max

from bot_for_trafic.base_conf import BaseConf

from .models import (
    Tweets,
    RoleUserTwitter,
    ReplyStatus,
    UserTwitter,
    ReplyText,
    StatusFilterText)
from .utils.decorators import CustomCeleryTask
from .utils.twitter_access import TwitterAccess
from .utils.twitter_module import BotTwitter

logger = get_task_logger(__name__)


@CustomCeleryTask(name="tasks.search_tweet_by_text")
def search_tweet_by_text(id_args, base_text=None):
    base_text = base_text or BaseConf.BASE_TEXT_FOR_SEARCH

    twitter_access = TwitterAccess(RoleUserTwitter.ADMIN)

    consumer_key_ = twitter_access.get_consumer_key
    consumer_secret_ = twitter_access.get_consumer_secret
    access_token_ = twitter_access.get_access_token
    access_token_secret_ = twitter_access.get_access_token_secret
    dict_count_use = {"count_use": twitter_access.get_access_token_secret + 1}
    id_record = twitter_access.get_id

    if not id_record:
        logger.error("[e] search_tweet_by_text - Can't get auth")
        return False

    try:
        bot_object = BotTwitter(
            consumer_key=consumer_key_,
            consumer_secret=consumer_secret_,
            access_token=access_token_,
            access_token_secret=access_token_secret_)

        max_id = Tweets.objects.filter().aggregate(max_id=Max('id_tweet'))
        bot_object.search_by_text(base_text, max_id=max_id.get('max_id'))

    except Exception as err:
        logger.error("[e] search_tweet_by_text - Bot twitter finish work with error. {}".format(err))
        UserTwitter.objects.filter(pk=id_record).update(**dict_count_use)
        return False

    UserTwitter.objects.filter(pk=id_record).update(**dict_count_use)

    return True


@CustomCeleryTask(name="tasks.reply_for_tweet")
def reply_for_tweet(id_tweet):
    twitter_access = TwitterAccess(RoleUserTwitter.USER)

    consumer_key_ = twitter_access.get_consumer_key
    consumer_secret_ = twitter_access.get_consumer_secret
    access_token_ = twitter_access.get_access_token
    access_token_secret_ = twitter_access.get_access_token_secret
    dict_count_use = {"count_use": twitter_access.get_access_token_secret + 1}
    id_record = twitter_access.get_id

    if not id_record:
        logger.error("[e] search_tweet_by_text - Can't get auth")
        return False

    tweet = Tweets.objects.filter(
        id_tweet=id_tweet,
        status=StatusFilterText.ENABLE,
        id_reply__isnull=True
    ).values(
        'name_screen'
    ).first()

    if not tweet and tweet.get("name_screen") is None:
        logger.error("[e] reply_for_tweet - Can't get reply tweet")
        return False

    base_text = ReplyText.objects.filter(id_status=ReplyStatus.ENABLE).order_by('?').first()

    if base_text is None or not base_text.text:
        logger.error("[e] reply_for_tweet - Can't get reply text")
        return False

    try:
        bot_object = BotTwitter(
            consumer_key=consumer_key_,
            consumer_secret=consumer_secret_,
            access_token=access_token_,
            access_token_secret=access_token_secret_)
        bot_object.reply_for_tweet_by_id(
            tweet_id=id_tweet,
            text_response=base_text.text,
            user_name=tweet.get("name_screen"))
    except Exception as err:
        logger.error("[e] reply_on_tweet - Bot twitter finish work with error. {}".format(err))
        UserTwitter.objects.filter(id=id_record).update(**dict_count_use)
        return False

    UserTwitter.objects.filter(pk=id_record).update(**dict_count_use)
    dict_reply_tweet = {"id_reply": ReplyText.objects.get(pk=base_text.pk)}
    Tweets.objects.filter(id_tweet=id_tweet).update(**dict_reply_tweet)
    return True
