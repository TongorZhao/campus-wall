from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('分类名', max_length=50, unique=True)
    slug = models.SlugField('URL别名', max_length=50, unique=True)
    description = models.TextField('描述', blank=True)
    icon = models.CharField('图标', max_length=50, blank=True, help_text='Bootstrap icon class')
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def post_count(self):
        return self.posts.filter(is_deleted=False).count()


class Tag(models.Model):
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField('URL别名', max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def post_count(self):
        return self.posts.filter(is_deleted=False).count()


class Post(models.Model):
    ANONYMITY_CHOICES = [
        ('public', '公开'),
        ('anonymous', '匿名'),
    ]

    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='作者',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='分类',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='标签')
    anonymity = models.CharField('匿名状态', max_length=10, choices=ANONYMITY_CHOICES, default='public')
    is_pinned = models.BooleanField('置顶', default=False)
    is_deleted = models.BooleanField('已删除', default=False)
    view_count = models.PositiveIntegerField('浏览数', default=0)
    like_count = models.PositiveIntegerField('点赞数', default=0)
    comment_count = models.PositiveIntegerField('评论数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title

    def get_author_display(self):
        if self.anonymity == 'anonymous':
            return '匿名用户'
        return self.author.get_display_name()

    def get_author_avatar(self):
        if self.anonymity == 'anonymous':
            return None
        return self.author.avatar

    def increment_views(self):
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('图片', upload_to='posts/%Y/%m/')
    order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '帖子图片'
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return f'Image for {self.post.title}'


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user} likes {self.post}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='帖子',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='作者',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='父评论',
    )
    content = models.TextField('内容')
    anonymity = models.CharField('匿名状态', max_length=10, choices=Post.ANONYMITY_CHOICES, default='public')
    like_count = models.PositiveIntegerField('点赞数', default=0)
    is_deleted = models.BooleanField('已删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    def get_author_display(self):
        if self.anonymity == 'anonymous':
            return '匿名用户'
        return self.author.get_display_name()

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])


class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = '评论点赞'
        verbose_name_plural = verbose_name


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} favorited {self.post}'
