from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model

from . import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["email", "username"]

class BookshelfSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Bookshelf
        fields = ["id", "user", "title", "color"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request.user:
            bookshelf = models.Bookshelf(**validated_data)
            bookshelf.user = request.user
            return bookshelf
        else:
            raise AuthenticationFailed

    def update(self, instance, validated_data):
        bookshelf = super().update(instance, validated_data)

        request = self.context.get("request")
        if request.user == bookshelf.user:
            return bookshelf
        else:
            raise AuthenticationFailed


class OriginBookSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.OriginalBook
        fields = ["id", "isbn", "title", "publisher", "author", "thumbnail"]
        read_only_fields = []


class BookshelfBookSerializer(serializers.ModelSerializer):
    bookshelf = BookshelfSerializer()
    origin = OriginBookSerializer()

    class Meta:
        models = models.Book
        fields = ["id", "bookshelf", "isbn", "have", "origin"]
        read_only_fields = []