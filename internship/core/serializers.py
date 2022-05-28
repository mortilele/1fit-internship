from rest_framework import serializers
from rest_framework.authtoken.models import Token

from internship.core.models import Company, CompanyReview, CustomUser
from internship.utils.date import get_age


# Auth Serializers
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password',
            'birth_date'
        )
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'birth_date': {'write_only': True},
        }

    def validate_birth_date(self, value):
        if not value:
            raise serializers.ValidationError('Birth date is required')
        if get_age(value) < 16:
            raise serializers.ValidationError('Вам еще не исполнилось 16 лет')
        return value

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError('Username is required')
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('User with that username already exists')
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            birth_date=validated_data['birth_date']
        )
        Token.objects.get_or_create(user=user)
        return user


class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(
        read_only=True
    )
    username = serializers.CharField(
        write_only=True,
    )
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = CustomUser.objects.filter(
            username=validated_data['username']
        ).first()
        if not user:
            raise serializers.ValidationError('User does not exists')
        is_valid_password = user.check_password(validated_data['password'])
        if not is_valid_password:
            raise serializers.ValidationError('Invalid password')
        token, _ = Token.objects.get_or_create(user=user)
        validated_data['token'] = token.key
        return validated_data


# Company Serializers
class CompanyListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField()

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'kind',
            'logo',
            'avg_rating'
        )


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'kind',
            'logo',
            'created_at'
        )


# CompanyReview Serializers
class CompanyReviewListSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(
        source='author.email'
    )

    class Meta:
        model = CompanyReview
        fields = (
            'id',
            'value',
            'text',
            'created_at',
            'author_email'
        )
        read_only_fields = fields


class CompanyReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CompanyReview
        fields = (
            'value',
            'text',
            'company',
            'author'
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if CompanyReview.objects.filter(
                author=validated_data['author'],
                company=validated_data['company']
        ).exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв о данной компании')
        return validated_data


class CompanyReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = (
            'value',
            'text'
        )
