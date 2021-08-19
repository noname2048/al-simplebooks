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
    color = models.CharField(max_length=10, blank=True)


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

class CommentForBook(TimeStampedModel):
    """책에 대한 코멘트. 오리진 책에 대해 코멘트한다.
    1. 사용자
    2. 책
    3. 내용
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.deletion)
    book = models.ForeignKey("OriginBook", on_delete=models.deletion)
    content = models.CharField(max_length=400)

class CommentForBookshelf(TimeStampedModel):
    """책장에 대한 코멘트. 책장에 대해 코멘트한다.
    1. 사용자
    2. 책장
    3. 내용
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.deletion)
    bookshelf = models.ForeignKey("Bookshelf", on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
