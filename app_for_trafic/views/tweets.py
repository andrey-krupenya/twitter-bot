import logging

from django.db.models import Max
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from django.utils.translation import ugettext as _

from bot_for_trafic.base_conf import BaseConf
from ..serializers.query_text import SearchText
from ..tasks import reply_for_tweet
from ..models import UserTwitter, Tweets, RoleUserTwitter
from ..utils.auth import CustomTokenAuthentication
from ..utils.twitter_module import BotTwitter

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    tags=['CheckCredentialsForAccess'],
    operation_id='check_credential',
    operation_description='Check credentials | '
                          'GET check_user/{user_id}',
    responses={
        status.HTTP_202_ACCEPTED: openapi.Response(description=_("Rout for checking credentials")),
        status.HTTP_403_FORBIDDEN: openapi.Response(description=_("No such token")),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description=_("No such token"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                })
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description=_("Error description"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                })
        ),
    }
)
@api_view(['GET'])
@authentication_classes((CustomTokenAuthentication, ))
def credential_for_access(request, user_id):
    data_auth = UserTwitter.objects.filter(
        pk=user_id
    ).values(
        'name', 'consumer_key', 'consumer_secret', 'access_token',
        'access_token_secret', 'id_role__name', 'id_status__status'
    ).first()

    if not data_auth.exists():
        return JsonResponse(data={"message": f"Wrong user ID: {user_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    consumer_key_ = data_auth.get('consumer_key')
    consumer_secret_ = data_auth.get('consumer_secret')
    access_token_ = data_auth.get('access_token')
    access_token_secret_ = data_auth.get('access_token_secret')

    try:
        bot_object = BotTwitter(consumer_key=consumer_key_,
                                consumer_secret=consumer_secret_,
                                access_token=access_token_,
                                access_token_secret=access_token_secret_)
        name_user = bot_object.get_name_user()._json
        # bot_object.listener_tweets()
        return JsonResponse(data=name_user, status=status.HTTP_200_OK)
    except Exception as err:
        logger.error("[e] credential_for_access - Bot twitter not init. {}".format(err))
        return JsonResponse(data={"message": f"Error: {err}"},
                            status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='POST',
    tags=['SearchByQueryString'],
    operation_id='search_by_query_string',
    operation_description='Search by query string | '
                          'GET search_text/{user_id}',
    request_body=SearchText,
    responses={
        status.HTTP_202_ACCEPTED: openapi.Response(description=_("Search tweets by query text")),
        status.HTTP_403_FORBIDDEN: openapi.Response(description=_("No such token")),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description=_("No such token"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                })
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description=_("Error description"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                })
        ),
    }
)
@api_view(['POST'])
@authentication_classes((CustomTokenAuthentication, ))
def search_by_query_string(request, user_id):
    serializer = SearchText(data=request.data)

    if not serializer.is_valid():
        logger.error(serializer.errors)
        return JsonResponse(data={"error": serializer.errors, "status": "failed"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    data_auth = UserTwitter.objects.filter(
        pk=user_id,
        id_role=RoleUserTwitter.ADMIN
    ).values(
        'name', 'consumer_key', 'consumer_secret',
        'access_token', 'access_token_secret',
        'id_role__name', 'id_status__status'
    ).first()

    if not data_auth.exists():
        return JsonResponse(data={"message": f"Wrong ID Twitter User: {user_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    consumer_key_ = data_auth.get('consumer_key')
    consumer_secret_ = data_auth.get('consumer_secret')
    access_token_ = data_auth.get('access_token')
    access_token_secret_ = data_auth.get('access_token_secret')
    try:
        bot_object = BotTwitter(consumer_key=consumer_key_,
                                consumer_secret=consumer_secret_,
                                access_token=access_token_,
                                access_token_secret=access_token_secret_)

        max_id = Tweets.objects.filter().aggregate(max_id=Max('id_tweet'))
        id_tweets = bot_object.search_by_text(
            serializer.data.get("searchTextInTweets"),
            max_id=max_id.get('max_id')
        )

        for _ in id_tweets:
            reply_for_tweet.apply_async(args=[str(_)], countdown=15, retry=True,
                                        retry_policy=BaseConf.retry_policy,
                                        queue="reply_tweet")

        return JsonResponse(data=id_tweets, status=status.HTTP_200_OK)
    except Exception as err:
        logger.error("[e] credential_for_access - Bot twitter not init. {}".format(err))
        return JsonResponse(data={"message": f"Error: {err}"},
                            status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='POST',
    tags=['TestReply'],
    operation_id='send_test_reply',
    operation_description='Sent test reply message | '
                          'GET send_test_reply/{tweet_id}',
    request_body=SearchText,
    responses={
        status.HTTP_202_ACCEPTED: openapi.Response(description=_("Test reply")),
        status.HTTP_403_FORBIDDEN: openapi.Response(description=_("No such token")),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description=_("No such token"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                })
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description=_("Error description"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                })
        ),
    }
)
@api_view(['POST'])
@authentication_classes((CustomTokenAuthentication, ))
def reply_on_tweet(request, tweet_id):
    data_auth = UserTwitter.objects.filter(
        id_role=RoleUserTwitter.USER
    ).order_by(
        'count_use'
    ).values(
        'name', 'consumer_key',
        'consumer_secret',
        'access_token',
        'access_token_secret',
        'id_role__name',
        'id_status__status',
        'count_use', 'id'
    ).first()

    if not data_auth.exists():
        return JsonResponse(data={"message": f"Can't get auth"},
                            status=status.HTTP_404_NOT_FOUND)

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
    except Exception as err:
        logger.error("[e] reply_on_tweet - Bot twitter finish work with error. {}".format(err))
        UserTwitter.objects.filter(pk=id_record).update(**dict_count_use)
        return JsonResponse(data={"message": f"Error: {err}"},
                            status=status.HTTP_404_NOT_FOUND)

    UserTwitter.objects.filter(pk=id_record).update(**dict_count_use)

    logger.info("Finish work ")
    return JsonResponse(data={"message": f"Work do!"}, status=status.HTTP_200_OK)
