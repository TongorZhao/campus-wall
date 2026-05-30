from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=30, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', max_length=500, blank=True)
    school = models.CharField('学校', max_length=100, blank=True)
    grade = models.CharField('年级', max_length=50, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    is_verified = models.BooleanField('已认证', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.nickname or self.username

    def get_display_name(self):
        return self.nickname or self.username


class FollowRelationship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = '关注关系'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.follower} -> {self.following}'
