from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ping, ArticleListView, PostReadOnlyViewSet

router = DefaultRouter()

router.register("posts", PostReadOnlyViewSet, basename="post")

urlpatterns = [
    path("ping", ping),
    path("articles", ArticleListView.as_view(), name="articles_list"),
]

urlpatterns += router.urls
