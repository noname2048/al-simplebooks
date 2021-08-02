from django.contrib import admin

from . import models

@admin.register(models.Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "color")