from django.contrib import admin
from .models import Conversation, Message, AIConfig


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'sender_type', 'content', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'updated_at')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'sender_type', 'content', 'is_read', 'created_at')
    list_filter = ('is_read', 'sender_type', 'created_at')
    search_fields = ('content',)
    raw_id_fields = ('conversation', 'sender')


@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_name', 'is_enabled', 'updated_at')
    list_filter = ('is_enabled',)
    raw_id_fields = ('user',)
