from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

app_name = "simplebooks"

router = DefaultRouter()
router.register("", views.BookshelfViewSet, basename="bookshelf")
# router.register("bookshelf/<int:pk>/", views.BookshelfBookViewSet, basename="book")

urlpatterns = [
    path("recent/", views.RecentBookshelfListView.as_view(), name="recent"),
    path("", include(router.urls)),
]
