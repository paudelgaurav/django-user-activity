from django.core.management.base import BaseCommand, CommandError

from ...models import Article, Post


class Command(BaseCommand):
    help = "Seeding data for Post and Article models"

    def handle(self, *args, **options):
        post_bulk_create_list = [
            Post(**{"title": f"Title {i}", "body": f"Body {i}"}) for i in range(0, 5)
        ]
        article_bulk_create_list = [
            Article(**{"title": f"Title {i}", "body": f"Body {i}"}) for i in range(0, 5)
        ]
        Post.objects.bulk_create(post_bulk_create_list)
        Article.objects.bulk_create(article_bulk_create_list)
