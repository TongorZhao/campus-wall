from django.db import models
from django.conf import settings


class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name='参与者',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '对话'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return f'Conversation {self.pk}'

    def get_other_participant(self, user):
        return self.participants.exclude(pk=user.pk).first()

    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ('user', '用户'),
        ('ai', 'AI'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='对话',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='发送者',
    )
    sender_type = models.CharField(
        '发送者类型',
        max_length=10,
        choices=SENDER_TYPE_CHOICES,
        default='user',
    )
    content = models.TextField('内容')
    is_read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', '-created_at']),
        ]

    def __str__(self):
        return f'{self.sender}: {self.content[:50]}'

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])


class AIConfig(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_config',
        verbose_name='用户',
    )
    api_key = models.CharField('API密钥', max_length=500, blank=True, default='')
    api_base_url = models.URLField(
        'API地址',
        max_length=500,
        blank=True,
        default='https://api.openai.com/v1',
        help_text='OpenAI兼容的API地址，如 https://api.openai.com/v1',
    )
    model_name = models.CharField(
        '模型名称',
        max_length=100,
        blank=True,
        default='gpt-3.5-turbo',
        help_text='如 gpt-3.5-turbo, gpt-4, deepseek-chat 等',
    )
    system_prompt = models.TextField(
        '系统提示词',
        max_length=2000,
        blank=True,
        default='你是一个友善的AI助手，请用中文回答问题。',
        help_text='AI的角色设定和行为指南',
    )
    is_enabled = models.BooleanField('启用AI对话', default=False)
    temperature = models.FloatField(
        '温度',
        default=0.7,
        help_text='0.0-2.0，越高越随机',
    )
    max_tokens = models.PositiveIntegerField(
        '最大回复长度',
        default=1024,
        help_text='AI单次回复的最大token数',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = 'AI配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.get_display_name()} 的AI配置'

    def is_configured(self):
        return bool(self.api_key and self.api_base_url and self.model_name)
