#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import string
import emoji


def strip_emoji(raw_str):
    """
    Remove EMODJI symbol and chinese symbol too
    :param raw_str: tetx with all symbol
    :return: text clean
    """
    if raw_str is None:
        return raw_str

    try:
        emoji_pattern = re.compile(
            u"(\u0001[\uF300-\uF64F])|"
            u"(\u0001[\uF680-\uF6FF])|"
            u"(\uf480[\u8080-\u83BF])|"  # Liuda remarks
            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
            u"(\uD83E[\uDD00-\uDDFF])|"
            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
            u"(\ud83c[\udde0-\uddff])|"  # flags (iOS)
            u"([\u2934\u2935]\uFE0F?)|"
            u"([\u3030\u303D]\uFE0F?)|"
            u"([\u3297\u3299]\uFE0F?)|"
            u"([\u203C\u2049]\uFE0F?)|"
            u"([\u00A9\u00AE]\uFE0F?)|"
            u"([\u2122\u2139]\uFE0F?)|"
            u"(\uD83C\uDC04\uFE0F?)|"
            u"(\uD83C\uDCCF\uFE0F?)|"
            u"([\u0023\u002A\u0030-\u0039]\uFE0F?\u20E3)|"
            u"(\u24C2\uFE0F?|[\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55]\uFE0F?)|"
            u"([\u2600-\u26FF]\uFE0F?)|"
            u"([\u2700-\u27BF]\uFE0F?)"
            "+", flags=re.UNICODE)
        raw_str = emoji_pattern.sub(r'', raw_str)
        emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        regexp_emoji = re.compile('|'.join(re.escape(p) for p in emojis_list))
        raw_str = regexp_emoji.sub(r'', raw_str)
        return raw_str
    except Exception as err:
        pass
    return raw_str


def filter_printable_char(raw_str):
    """
    Remove non-printable char
    :param raw_str: str
        Raw text
    :return: str
        Clean text
    """
    if raw_str:
        return ''.join(x for x in strip_emoji(raw_str) if x in string.printable)
    return raw_str
