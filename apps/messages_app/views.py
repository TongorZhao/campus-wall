from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max, Count
from .models import Conversation, Message
from apps.accounts.models import User
from apps.notifications.models import Notification


@login_required
def conversation_list_view(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants').annotate(
        last_message_time=Max('messages__created_at'),
        unread_count=Count(
            'messages',
            filter=~Q(messages__sender=request.user) & Q(messages__is_read=False)
        )
    ).order_by('-last_message_time')

    for conv in conversations:
        conv.other_user = conv.participants.exclude(pk=request.user.pk).first()

    return render(request, 'messages/list.html', {
        'conversations': conversations,
    })


@login_required
def start_conversation_view(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        messages.error(request, '不能和自己发私信')
        return redirect('posts:feed')

    existing = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=target_user
    ).first()

    if existing:
        return redirect('messages:detail', pk=existing.pk)

    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, target_user)

    return redirect('messages:detail', pk=conversation.pk)


@login_required
def conversation_detail_view(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('participants'),
        pk=pk,
        participants=request.user,
    )

    other_user = conversation.get_other_participant(request.user)

    conversation.messages.filter(
        sender=other_user, is_read=False
    ).update(is_read=True)

    msg_list = conversation.messages.select_related('sender').all()

    return render(request, 'messages/detail.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages_list': msg_list,
    })


@login_required
def send_message_view(request, pk):
    if request.method != 'POST':
        return redirect('messages:detail', pk=pk)

    conversation = get_object_or_404(
        Conversation,
        pk=pk,
        participants=request.user,
    )

    content = request.POST.get('content', '').strip()
    if not content:
        messages.error(request, '消息内容不能为空')
        return redirect('messages:detail', pk=pk)

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=content,
    )

    conversation.save()

    other_user = conversation.get_other_participant(request.user)
    if other_user:
        Notification.objects.create(
            user=other_user,
            notification_type='system',
            actor=request.user,
            message=f'{request.user.get_display_name()} 给你发了一条私信',
        )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'sender': message.sender.get_display_name(),
                'created_at': message.created_at.strftime('%m-%d %H:%M'),
            }
        })

    return redirect('messages:detail', pk=pk)


@login_required
def mark_conversation_read_view(request, pk):
    if request.method != 'POST':
        return redirect('messages:detail', pk=pk)

    conversation = get_object_or_404(
        Conversation,
        pk=pk,
        participants=request.user,
    )

    other_user = conversation.get_other_participant(request.user)
    if other_user:
        conversation.messages.filter(sender=other_user, is_read=False).update(is_read=True)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('messages:detail', pk=pk)
