#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import time

from markupsafe import escape

from bot_for_trafic.base_conf import BaseConf

logger = logging.getLogger(__name__)


class SendMessageToBot(object):
    site_name = "Services Messages"

    @staticmethod
    def anti_escape(s):
        """
        Convert the characters &#39;, &#34; in to ' and ".
        :param s: escaped text
        :return: anti escaped text
        """
        return str(s).replace('&#39;', "'").replace('&#34;', '"')

    def sent_text_to_telegram(self, record, comment=None):
        """
        SEND text to TELEGRAM BOT.
        :param record: WARNING/ERROR text
        :param comment: comment for Error/Warning
        :return: result request to telegram
        """
        try:
            if comment:
                message_err = self.anti_escape(escape("{0}. Comment:[{1}]".format(record, comment)))
            else:
                message_err = self.anti_escape(escape("{}".format(record)))
            token = BaseConf.telegram_token
            url = 'https://api.telegram.org/{0}/sendMessage'.format(token)

            data = {
                'text': '<b>{2}\n date time: {0}</b>\n{1}'.format(
                    time.strftime('%Y-%m-%d %H:%M:%S'), message_err,
                    self.site_name),
                'parse_mode': 'HTML',
                'chat_id': BaseConf.telegram_chat_id
            }
            k = requests.post(url, data=data)
            return k
        except Exception as err:
            logger.error("[e] {}".format(err))
        return None
