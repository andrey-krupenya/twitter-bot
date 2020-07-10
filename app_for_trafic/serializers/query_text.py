from rest_framework import serializers


class SearchText(serializers.Serializer):
    searchTextInTweets = serializers.CharField(required=True)
