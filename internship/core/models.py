from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from internship.utils.model_mixins import TimeStampedMixin


class CustomUser(AbstractUser):
    birth_date = models.DateField(
        verbose_name='Date of Birth'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Company(TimeStampedMixin):
    class Kind(models.TextChoices):
        IE = "IE", "Individual Entrepreneur"
        JSC = "JSC", "Joint-Stock Company"
        LLC = "LLC", "Limited Liability Company"

    name = models.CharField(
        verbose_name='Name',
        max_length=50
    )
    kind = models.CharField(
        verbose_name='Kind',
        max_length=3,
        choices=Kind.choices,
        default=Kind.IE
    )
    logo = models.ImageField(
        verbose_name='Logo'
    )
    owner = models.OneToOneField(
        CustomUser,
        verbose_name='Owner',
        on_delete=models.PROTECT,
        related_name='company'
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self) -> str:
        return self.name


class CompanyReview(TimeStampedMixin):
    value = models.PositiveSmallIntegerField(
        verbose_name='Value',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(5)
        )
    )
    text = models.TextField(
        verbose_name='Review text',
        blank=True,
        null=True
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Company',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='company_reviews'
    )

    class Meta:
        verbose_name = "Company's review"
        verbose_name_plural = "Company's reviews"

    def __str__(self) -> str:
        return f'{self.value} - {self.text}'
