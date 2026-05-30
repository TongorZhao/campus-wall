def unread_message_count(request):
    if request.user.is_authenticated:
        from django.db.models import Q, Count
        from .models import Conversation
        count = Conversation.objects.filter(
            participants=request.user
        ).annotate(
            unread=Count(
                'messages',
                filter=~Q(messages__sender=request.user) & Q(messages__is_read=False)
            )
        ).values_list('unread', flat=True)
        total = sum(count)
        return {'unread_message_count': total}
    return {'unread_message_count': 0}
