from django.contrib import admin

from . import models


@admin.register(models.Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "color")


@admin.register(models.OriginalBook)
class OriginalBookAdmin(admin.ModelAdmin):
    list_display = ("isbn", "title")


@admin.register(models.CommentForBookshelf)
class CommentForBookshelfAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bookshelf", "content")
