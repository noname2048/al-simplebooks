from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

app_name = "simplebooks"

router = DefaultRouter()
router.register("bookshelf", views.BookshelfViewSet, basename="bookshelf")
router.register("bookshelf/(?P<bookshelf_pk>[0-9]+)/book", views.BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
]
