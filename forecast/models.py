from django.db import models


class Search(models.Model):
    session_key = models.CharField(
        max_length=40,
        db_index=True,
        )
    city = models.CharField(
        max_length=100,
        db_index=True,
        )
    searched_at = models.DateTimeField(
        auto_now_add=True,
        )

    class Meta:
        ordering = ('-searched_at',)
