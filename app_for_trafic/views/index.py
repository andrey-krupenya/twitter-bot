#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from ..models import UserTwitter, Tweets
from ..utils.twitter_module import BotTwitter


def index_page(request):
    return render(request, "index.html", {})


def credential_for_access(request, user_id):
    data_auth = UserTwitter.objects.filter(pk=user_id).values('name', 'consumer_key', 'consumer_secret', 'access_token',
                                                              'access_token_secret', 'id_role__name',
                                                              'id_status__status')
    if not data_auth.exists():
        return HttpResponse('Wrong ID Twitter User!')
    consumer_key_ = data_auth[0].get('consumer_key')
    consumer_secret_ = data_auth[0].get('consumer_secret')
    access_token_ = data_auth[0].get('access_token')
    access_token_secret_ = data_auth[0].get('access_token_secret')
    try:
        bot_object = BotTwitter(consumer_key=consumer_key_,
                                consumer_secret=consumer_secret_,
                                access_token=access_token_,
                                access_token_secret=access_token_secret_)
        name_user = bot_object.get_name_user()._json
        # bot_object.listener_tweets()
        return JsonResponse(data=name_user, status=200)
    except Exception as e:
        logging.error("[e] credential_for_access - Bot twitter not init. {}".format(e))
        return HttpResponse('Some error! {}'.format(e))


def search_by_query_string(request, user_id, search_text_in_twits):
    data_auth = UserTwitter.objects.filter(pk=user_id, id_role=2).values('name', 'consumer_key', 'consumer_secret',
                                                                         'access_token', 'access_token_secret',
                                                                         'id_role__name', 'id_status__status')
    if not data_auth.exists():
        return HttpResponse('Wrong ID Twitter User!')
    consumer_key_ = data_auth[0].get('consumer_key')
    consumer_secret_ = data_auth[0].get('consumer_secret')
    access_token_ = data_auth[0].get('access_token')
    access_token_secret_ = data_auth[0].get('access_token_secret')
    try:
        bot_object = BotTwitter(consumer_key=consumer_key_,
                                consumer_secret=consumer_secret_,
                                access_token=access_token_,
                                access_token_secret=access_token_secret_)
        max_id = Tweets.objects.filter().aggregate(max_id=Max('id_tweet'))
        find_tweets = bot_object.search_by_text(search_text_in_twits, max_id=max_id.get('max_id'))
        return JsonResponse(data=find_tweets, status=200)
    except Exception as e:
        logging.error("[e] credential_for_access - Bot twitter not init. {}".format(e))
        return HttpResponse('Some error!')


def test_reply_tweet(request, tweet_id):
    data_auth = UserTwitter.objects.filter(id_role=1).order_by('count_use').values('name', 'consumer_key',
                                                                                   'consumer_secret',
                                                                                   'access_token',
                                                                                   'access_token_secret',
                                                                                   'id_role__name',
                                                                                   'id_status__status',
                                                                                   'count_use', 'id')[0]
    if not data_auth:
        logging.error("[e] test_reply_tweet - Can't get auth")
        return False
    consumer_key_ = data_auth.get('consumer_key')
    consumer_secret_ = data_auth.get('consumer_secret')
    access_token_ = data_auth.get('access_token')
    access_token_secret_ = data_auth.get('access_token_secret')
    dict_count_use = {"count_use": int(data_auth.get('count_use')) + 1}
    id_record = data_auth.get('id')
    tweet = Tweets.objects.get(id_tweet=tweet_id)
    try:
        bot_object = BotTwitter(consumer_key=consumer_key_,
                                consumer_secret=consumer_secret_,
                                access_token=access_token_,
                                access_token_secret=access_token_secret_)
        bot_object.reply_for_tweet_by_id(tweet_id=tweet_id,
                                         text_response="Hi! I can help you!!!",
                                         user_name=tweet.name_screen)
    except Exception as e:
        logging.error("[e] test_reply_tweet - Bot twitter finish work with error. {}".format(e))
        UserTwitter.objects.filter(id=id_record).update(**dict_count_use)
        return HttpResponse('Some error!')
    UserTwitter.objects.filter(id=id_record).update(**dict_count_use)
    logging.info("Finish work ")
    return HttpResponse('Work do!')
