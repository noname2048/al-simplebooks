from django.db.models import query
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import response
from rest_framework import permissions
from rest_framework import status
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
        obj = get_object_or_404(queryset, **{"pk": kwargs.get("pk")})
        serializer = serializers.BookshelfSerializer(instance=obj) 
        return response.Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        queryset = models.Bookshelf.objects.all()
        instance = get_object_or_404(queryset, **{"pk": kwargs.get("pk")})

        user = request.user if request.user.is_authenticated else get_user_model().objects.get(username="admin")
        if instance.user != user:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.BookshelfSerializer(instance=instance, data=request.POST, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)

        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        queryset = models.Bookshelf.objects.all()
        obj = get_object_or_404(queryset, **{"pk": kwargs.get("pk")})
        
        user = request.user if request.user.is_authenticated else get_user_model().objects.get(username='admin')
        if user == obj.user:
            obj.delete()
            return response.Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return response.Response(None, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        return [permission() for permission in [permissions.AllowAny]]

        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action in ["create", "update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]