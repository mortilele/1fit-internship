from django.db import models


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Creation DateTime',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='DateTime of last modification',
        auto_now=True
    )

    class Meta:
        abstract = True
