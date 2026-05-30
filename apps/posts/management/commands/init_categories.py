from django.core.management.base import BaseCommand
from apps.posts.models import Category


class Command(BaseCommand):
    help = '初始化校园墙默认分类'

    def handle(self, *args, **options):
        categories = [
            {'name': '表白墙', 'slug': 'confession', 'icon': 'bi-heart', 'order': 1},
            {'name': '失物招领', 'slug': 'lost-found', 'icon': 'bi-search', 'order': 2},
            {'name': '二手交易', 'slug': 'trade', 'icon': 'bi-bag', 'order': 3},
            {'name': '吐槽树洞', 'slug': 'vent', 'icon': 'bi-chat-heart', 'order': 4},
            {'name': '学习交流', 'slug': 'study', 'icon': 'bi-book', 'order': 5},
            {'name': '社团活动', 'slug': 'club', 'icon': 'bi-people', 'order': 6},
            {'name': '表白墙', 'slug': 'confession2', 'icon': 'bi-envelope-heart', 'order': 7},
            {'name': '校园资讯', 'slug': 'news', 'icon': 'bi-megaphone', 'order': 8},
            {'name': '其他', 'slug': 'other', 'icon': 'bi-three-dots', 'order': 99},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建分类: {category.name}'))
            else:
                self.stdout.write(f'分类已存在: {category.name}')

        self.stdout.write(self.style.SUCCESS('分类初始化完成'))
