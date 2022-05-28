from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from internship.core.models import Company, CompanyReview
from internship.core.serializers import CompanyListSerializer, CompanyDetailSerializer, CompanyReviewCreateSerializer, \
    CompanyReviewListSerializer, CompanyReviewUpdateSerializer, UserCreateSerializer, ObtainTokenSerializer
from internship.utils.permissions import IsSuperUser


class AuthViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin
):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'sign_in':
            return ObtainTokenSerializer

    def sign_in(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class CompanyViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    permissions = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('kind',)

    def get_queryset(self):
        return Company.objects.all().annotate(
            avg_rating=Avg('reviews__value')
        ).order_by('-avg_rating')

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyListSerializer
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return None


class CompanyReviewViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin
):
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('value',)
    lookup_field = 'company_id'
    lookup_url_kwarg = 'company_id'

    def get_queryset(self):
        queryset = CompanyReview.objects.all()
        if self.action == 'user_reviews':
            return queryset.filter(author=self.request.user)
        if self.action == 'list':
            lookup = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
            return queryset.filter(**lookup)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyReviewCreateSerializer
        if self.action == 'list':
            return CompanyReviewListSerializer
        if self.action == 'user_reviews':
            return CompanyReviewListSerializer
        if self.action == 'update':
            return CompanyReviewUpdateSerializer

    def get_permissions(self):
        if self.action == 'update':
            self.permission_classes = (IsAuthenticated, IsSuperUser)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def user_reviews(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance: CompanyReview = serializer.save()
        """Send an email to company owner."""
        instance.company.owner.email_user(
            subject='Вам оставили отзыв о компании',
            message=f'{instance.value} - {instance.text}'
        )
