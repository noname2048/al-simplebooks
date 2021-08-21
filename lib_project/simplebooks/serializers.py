from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.http import Http404
from django.contrib.auth import get_user_model

from . import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["email", "username"]


class BookshelfSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Bookshelf
        fields = ["id", "user", "title", "color"]

    def validate_user(self, value):
        request = self.context["request"]
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = "admin"

        user = get_user_model().objects.get(username=username)
        if not user.exists():
            raise HttpResponseBadRequest

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_authenticated:
            user = get_user_model().objects.get(username="admin")
        return models.Bookshelf.objects.create(**validated_data, user=user)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.color = validated_data.get("color", instance.color) 
        instance.save()

        return instance 


class OriginBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OriginalBook
        fields = ["isbn", "title", "publisher", "author", "thumbnail"]
        read_only_fields = []

    def __str__(self):
        return f"{self.title}({self.isbn})"


class BookshelfBookSerializer(serializers.ModelSerializer):
    bookshelf = BookshelfSerializer(read_only=True)
    origin = OriginBookSerializer(read_only=True)

    class Meta:
        model = models.Book
        fields = ["id", "bookshelf", "isbn", "have", "origin"]
        read_only_fields = []

    def create(self, validated_data):
        bookshelf_pk = self.context["bookshelf_pk"]
        return models.Book.objects.create(bookshelf_id=bookshelf_pk, **validated_data)


class CommentForBookshelfSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    bookshelf = BookshelfSerializer(read_only=True)

    class Meta:
        model = models.CommentForBookshelf
        fields = ["id", "user", "bookshelf", "content"]


class CommentForOriginalBookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.CommentForOriginalBook
        fields = ["id", "user", "original_book", "content"]
