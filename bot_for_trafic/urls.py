"""bot_for_trafic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from app_for_trafic.views import (index as IndexMethods)

urlpatterns = [
    url(r'^secure_admin_url/', admin.site.urls),
    url(r'^$', IndexMethods.index_page, name='index'),
    url(r'^check_user/(?P<user_id>\d+)$', IndexMethods.credential_for_access, name="check_user"),
    url(r'^search_text/(?P<user_id>\d+)/(?P<search_text_in_twits>\w+)$', IndexMethods.search_by_query_string,
        name="search_text_in_twits"),
    url(r'^send_test_reply/(?P<tweet_id>\d+)$', IndexMethods.test_reply_tweet, name="send_test_reply"),
    url(r'^robots.txt$', TemplateView.as_view(template_name="meta/robots.txt", content_type="text/plain"),
        name="robots_file"),
]
