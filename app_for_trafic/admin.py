# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (RoleUserTwitter, StatusTweet, StatusUserTwitter, Tweets, UserTwitter, FilterText, ReplyText,
                     ReplyStatus, StatusFilterText)

admin.site.register(RoleUserTwitter)
admin.site.register(StatusTweet)
admin.site.register(StatusUserTwitter)
admin.site.register(Tweets)
admin.site.register(UserTwitter)
admin.site.register(FilterText)
admin.site.register(ReplyText)
admin.site.register(ReplyStatus)
admin.site.register(StatusFilterText)

