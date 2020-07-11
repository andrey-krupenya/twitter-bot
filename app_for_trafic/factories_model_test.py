import factory
import random
import pytz

from app_for_trafic import models


class ReplyTextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ReplyText
        django_get_or_create = ('text',)

    text = factory.Faker('text', max_nb_chars=250, ext_word_list=None)
    id_status = factory.Iterator(models.ReplyStatus.objects.all())
    count_use = random.randint(1, 10)


class TweetsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tweets
        django_get_or_create = ('id_tweet',)

    id_tweet = random.randint(100000, 1000000000)
    id_user = random.randint(100000, 1000000000)
    name_author = factory.Faker('first_name')
    name_screen = factory.Faker('last_name')
    text_tweet = factory.Faker('text', max_nb_chars=250, ext_word_list=None)
    create_at = factory.Faker('date_time_between', tzinfo=pytz.UTC, start_date="-10d", end_date="-1d")
    location = factory.Faker('city')
    geo = factory.Faker('country_code', representation="alpha-2")
    source = factory.Faker('text', max_nb_chars=45, ext_word_list=None)
    lang = factory.Faker('text', max_nb_chars=3, ext_word_list=None)
    status = factory.Iterator(models.StatusTweet.objects.all())
    id_reply = factory.SubFactory(ReplyTextFactory)


class UserTwitterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tweets
        django_get_or_create = ('name_author',)

    name_author = factory.Faker('name')
    consumer_key = factory.Faker('text', max_nb_chars=50, ext_word_list=None)
    consumer_secret = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    access_token = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    access_token_secret = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    id_role = factory.Iterator(models.RoleUserTwitter.objects.all())
    id_status = factory.Iterator(models.StatusUserTwitter.objects.all())
    count_use = random.randint(1, 100)


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tweets
        django_get_or_create = ('nickname',)

    nickname = factory.Faker('first_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda o: '%s.%s@test.com' % (o.first_name.lower(), o.last_name.lower()))
    password = 'password'
    date = factory.Faker('date_time_between', tzinfo=pytz.UTC, start_date="-100d", end_date="-50d")
    phone = factory.Faker('msisdn')
    id_role = factory.Iterator(models.RoleUserTwitter.objects.all())
