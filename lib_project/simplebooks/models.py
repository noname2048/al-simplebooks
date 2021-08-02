from django.db import models
from django.conf import settings

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Bookshelf(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=10)


class Book(TimeStampedModel):
    bookshelf = models.ForeignKey("Bookshelf", on_delete=models.deletion.CASCADE)
    isbn = models.PositiveBigIntegerField()
    origin = models.ForeignKey("OriginalBook", on_delete=models.deletion.CASCADE, null=True)
    have = models.BooleanField(blank=True, default=False)


class OriginalBook(TimeStampedModel):
    isbn = models.PositiveBigIntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField()

    publisher = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
