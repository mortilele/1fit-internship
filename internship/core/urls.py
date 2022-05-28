from django.urls import path

from internship.core import views

urlpatterns = [
    path(
        "users/sign-up",
        views.AuthViewSet.as_view(
            {
                "post": "create"
            }
        ),
        name="sign-up"
    ),
    path(
        "users/sign-in",
        views.AuthViewSet.as_view(
            {
                "post": "sign_in"
            }
        ),
        name="sign-in"
    ),
    path(
        "companies",
        views.CompanyViewSet.as_view(
            {
                "get": "list"
            }
        ),
        name="company-list"
    ),
    path(
        "companies/<int:pk>",
        views.CompanyViewSet.as_view(
            {
                "get": "retrieve"
            }
        ),
        name="company-detail"
    ),
    path(
        "companies/reviews/",
        views.CompanyReviewViewSet.as_view(
            {
                "post": "create"
            }
        ),
        name="company-review-create"
    ),
    path(
        "companies/reviews/my",
        views.CompanyReviewViewSet.as_view(
            {
                "get": "user_reviews"
            }
        ),
        name="company-review-user-list"
    ),
    path(
        "companies/reviews/<int:pk>",
        views.CompanyReviewViewSet.as_view(
            {
                "put": "update"
            },
            lookup_field='pk',
            lookup_url_kwarg='pk'
        ),
        name="company-review-update"
    ),
    path(
        "companies/<int:company_id>/reviews/",
        views.CompanyReviewViewSet.as_view(
            {
                "get": "list"
            }
        ),
        name="company-review-list"
    ),

]