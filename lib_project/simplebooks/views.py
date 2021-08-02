from django.db.models import query
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from . import models

from django.contrib.auth import get_user, get_user_model
from . import serializers

from rest_framework.generics import ListAPIView

from django.utils import encoding


class RecentBookshelfListView(ListAPIView):

    queryset = models.Bookshelf.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = models.Bookshelf.objects.select_related("user").all()

        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = "admin"

        username = request.GET.get("username", username)
        queryset = queryset.filter(user__username__icontains=username)        
        
        q = request.GET.get("q")
        if q:
            queryset = queryset.filter(title__icontains=q)
        queryset = queryset.order_by("-updated_at")

        serializer = serializers.BookshelfSerializer(queryset[:10], many=True)
        return response.Response(serializer.data)
        

class BookshelfViewSet(viewsets.GenericViewSet):

    queryset = models.Bookshelf.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.user.is_authenticated:
            queryset = queryset.filter(username=request.user)
        else:
            return redirect()

        q = request.GET.get("q")
        if q:
            queryset.filter(title_icontains=q)
        
        queryset = queryset.order_by("-updated_at")
        serializer = serializers.BookshelfSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.BookshelfSerializer(data=request.POST, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        queryset = models.Bookshelf.objects.all()
        queryset = queryset.filter(pk=kwargs["pk"])
        bookshelf = get_object_or_404(queryset)
        return response.Response(bookshelf.values())

    def update(self, request, *args, **kwargs):
        queryset = models.Bookshelf.objects.all()
        queryset = queryset.filter(pk=kwargs["pk"])
        bookshelf = get_object_or_404(queryset)
        serializer = serializers.BookshelfSerializer(
            instance=bookshelf, data=request.POST, context={"request": request}
        )
        serializer.save()
        return serializer

    def destroy(self, request, *args, **kwargs):
        pass

    def get_permissions(self):
        return [permission() for permission in [permissions.AllowAny]]

        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action in ["create", "update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]