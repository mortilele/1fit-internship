from django.contrib import admin

from internship.core.models import CustomUser, Company, CompanyReview


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'birth_date')
    list_filter = ('is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kind', 'created_at', 'updated_at')
    list_filter = ('kind', 'created_at')
    search_fields = ('name', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CompanyReview)
class CompanyReview(admin.ModelAdmin):
    list_display = ('id', 'company', 'value', 'created_at', 'updated_at')
    list_filter = ('value', 'created_at')
    search_fields = ('company__name', 'author__email')
    readonly_fields = ('created_at', 'updated_at')
