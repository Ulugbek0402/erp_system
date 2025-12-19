from django.urls import path
from .views import (
    UserListCreateAPIView, UserDetailAPIView,
    CategoryListCreateAPIView, CategoryDetailAPIView,
    NewsListCreateAPIView, NewsDetailAPIView,
    CommitListCreateAPIView, CommitDetailAPIView,
)

urlpatterns = [
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("news/", NewsListCreateAPIView.as_view(), name="news-list-create"),
    path("news/<int:pk>/", NewsDetailAPIView.as_view(), name="news-detail"),
    path("commits/", CommitListCreateAPIView.as_view(), name="commit-list-create"),
    path("commits/<int:pk>/", CommitDetailAPIView.as_view(), name="commit-detail"),
]
