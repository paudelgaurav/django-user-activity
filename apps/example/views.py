from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.activity_log.mixins import ActivityLogMixin

from .models import Post, Article
from .serializers import PostSerializer


@api_view()
def ping(request):
    return Response("Pong")


class ArticleListView(ActivityLogMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response({"articles": Article.objects.values()})


class PostReadOnlyViewSet(ActivityLogMixin, ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_log_message(self, request) -> str:
        return f"{request.user} is reading blog posts"
