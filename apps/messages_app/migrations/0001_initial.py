from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('participants', models.ManyToManyField(related_name='conversations', to=settings.AUTH_USER_MODEL, verbose_name='参与者')),
            ],
            options={
                'verbose_name': '对话',
                'verbose_name_plural': '对话',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_type', models.CharField(choices=[('user', '用户'), ('ai', 'AI')], default='user', max_length=10, verbose_name='发送者类型')),
                ('content', models.TextField(verbose_name='内容')),
                ('is_read', models.BooleanField(default=False, verbose_name='已读')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messages_app.conversation', verbose_name='对话')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='发送者')),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['conversation', '-created_at'], name='messages_app_conversa_idx'),
        ),
        migrations.CreateModel(
            name='AIConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(blank=True, default='', max_length=500, verbose_name='API密钥')),
                ('api_base_url', models.URLField(blank=True, default='https://api.openai.com/v1', help_text='OpenAI兼容的API地址，如 https://api.openai.com/v1', max_length=500, verbose_name='API地址')),
                ('model_name', models.CharField(blank=True, default='gpt-3.5-turbo', help_text='如 gpt-3.5-turbo, gpt-4, deepseek-chat 等', max_length=100, verbose_name='模型名称')),
                ('system_prompt', models.TextField(blank=True, default='你是一个友善的AI助手，请用中文回答问题。', help_text='AI的角色设定和行为指南', max_length=2000, verbose_name='系统提示词')),
                ('is_enabled', models.BooleanField(default=False, verbose_name='启用AI对话')),
                ('temperature', models.FloatField(default=0.7, help_text='0.0-2.0，越高越随机', verbose_name='温度')),
                ('max_tokens', models.PositiveIntegerField(default=1024, help_text='AI单次回复的最大token数', verbose_name='最大回复长度')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ai_config', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': 'AI配置',
                'verbose_name_plural': 'AI配置',
            },
        ),
    ]
