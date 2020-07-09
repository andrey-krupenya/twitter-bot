#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from .utils.botsendmessage import SendMessageToBot


class TelegramLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        SendMessageToBot().sent_text_to_telegram("{}".format(self.format(record)))
        return True
