#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import logging

from datetime import datetime, timedelta

from ..models import StatusTweet, Tweets, FilterText
from ..utils.utils import strip_emoji, filter_printable_char
from ..utils.botsendmessage import SendMessageToBot
from ..tasks import reply_for_tweet

logger = logging.getLogger(__name__)


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status) -> None:
        logger.info(status.text)
        if 'manchester united' in status.text.lower():
            logger.info(status.text)

    def on_data(self, data) -> bool:
        logger.info("DATA: {}".format(data))
        return True

    def on_error(self, status_code) -> bool:
        logger.info('Encountered error with status code:{}'.format(status_code))
        return True  # Don't kill the stream

    def on_timeout(self) -> bool:
        logger.info('Timeout...')
        return True  # Don't kill the stream


class BotTwitter(object):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._auth = tweepy.OAuthHandler(self._consumer_key,
                                         self._consumer_secret)
        self._auth.set_access_token(self._access_token,
                                    self._access_token_secret)
        self._api = tweepy.API(self._auth)

    def get_name_user(self):
        """
        Return name user
        :return: str
            Name user
        """
        return self._api.me()

    def search_by_text(self, query_text: str, max_id: int = None) -> int:
        """
        Search tweets by some text
        :param query_text: str
            Text for search in twitter
        :param max_id: int
            Max ID tweet for search new tweets
        :return: list[dict]
            Data for work
        """
        text_list_include = FilterText.objects.filter(id_status=1).values_list('text') or []
        if not text_list_include:
            logging.error("[e] reply_for_tweet_by_id - Please check filter_text table or fix query")
            return 0
        text_list_exclude = FilterText.objects.filter(id_status=2).values_list('text') or []
        from_date = datetime.now() - timedelta(days=1)
        to_date = datetime.now() + timedelta(days=1)
        if max_id and max_id > 0:
            search_results = tweepy.Cursor(self._api.search,
                                           q=query_text,
                                           since=from_date.strftime("%Y-%m-%d"),
                                           until=to_date.strftime("%Y-%m-%d"),
                                           since_id=max_id,
                                           # monitor_rate_limit=True,
                                           # wait_on_rate_limit=True,
                                           result_type='recent',
                                           lang="en").items()
        else:
            search_results = tweepy.Cursor(self._api.search,
                                           q=query_text,
                                           since=from_date.strftime("%Y-%m-%d"),
                                           until=to_date.strftime("%Y-%m-%d"),
                                           # monitor_rate_limit=True,
                                           # wait_on_rate_limit=True,
                                           result_type='recent',
                                           lang="en").items()
        i = 0
        for item in search_results:
            try:
                tweet_text = filter_printable_char(strip_emoji(item.text))
                count_include = 0
                count_exclude = 0
                for item_text in text_list_include:
                    if str(''.join(item_text)).lower() in tweet_text.lower():
                        count_include = count_include + 1
                if len(text_list_include) > count_include:
                    continue
                for item_text in text_list_exclude:
                    if str(''.join(item_text)).lower() not in tweet_text.lower():
                        count_exclude = count_exclude + 1
                if len(text_list_exclude) > count_exclude:
                    continue
                if Tweets.objects.filter(id_tweet=item.id).exists():
                    continue
                i += 1
                dict_record = {"id_tweet": item.id,
                               "id_user": item.user.id,
                               "name_author": filter_printable_char(strip_emoji(item.user.name)),
                               "name_screen": item.user.screen_name,
                               "text_tweet": tweet_text,
                               "create_at": item.created_at if isinstance(item.created_at, datetime) else datetime.now(),
                               "location": filter_printable_char(strip_emoji(item.user.location)),
                               "geo": item.geo,
                               "source": filter_printable_char(item.source),
                               "lang": filter_printable_char(item.lang),
                               "status": StatusTweet.objects.get(id=1)}
                new_tweet = Tweets.objects.create(**dict_record)
                new_tweet.save()
                logging.info("Add {0} row. ID: {1}".format(i, new_tweet.pk))
                logging.info("MAX ID: {}".format(str(item.id)))
                reply_for_tweet.apply_async(args=[str(item.id)], countdown=15, retry=True,
                                            retry_policy={
                                                'max_retries': 5,
                                                'interval_start': 60 * 5,
                                                'interval_step': 60 * 15,
                                                'interval_max': 60 * 10,
                                                                     },
                                            queue="reply_tweet")
            except Exception as e:
                logging.exception("Error search_by_text. {}".format(e))
                i -= 1
                continue
        return i

    def listener_tweets(self):
        sapi = tweepy.streaming.Stream(self._auth, CustomStreamListener())
        sapi.filter(track=['essay'])
        # sapi.filter(locations=[-6.38, 49.87, 1.77, 55.81])

    def reply_for_tweet_by_id(self, tweet_id: int, text_response: str, user_name: str) -> bool:
        """
        Reply for tweet some user
        :param tweet_id: int
            ID tweet
        :param text_response: str
            Text for reply
        :param user_name: str
            Screen name user
        :return: bool
            Result operation
        """
        try:
            self._api.update_status("@{0} {1}".format(user_name, text_response), in_reply_to_status_id=tweet_id)
            return True
        except tweepy.TweepError as err:
            SendMessageToBot().sent_text_to_telegram("[e] reply_for_tweet_by_id - {}".format(err.reason))
            logger.error("[e] reply_for_tweet_by_id - {}".format(err.reason))
        return False
