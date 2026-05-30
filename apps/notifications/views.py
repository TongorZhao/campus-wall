from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Notification, Report


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user)

    notification_type = request.GET.get('type')
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)

    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)

    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'current_type': notification_type,
    })


@login_required
def mark_read_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    next_url = request.GET.get('next')
    if not next_url or not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = 'notifications:list'
    return redirect(next_url)


@login_required
def mark_all_read_view(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, '已全部标记为已读')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('notifications:list')


@login_required
def delete_notification_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, '通知已删除')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('notifications:list')


@login_required
def report_view(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_id = request.POST.get('comment_id')
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')

        report = Report(
            reporter=request.user,
            reason=reason,
            description=description,
        )
        if post_id:
            from apps.posts.models import Post
            report.post = get_object_or_404(Post, pk=post_id)
        if comment_id:
            from apps.posts.models import Comment
            report.comment = get_object_or_404(Comment, pk=comment_id)

        report.save()
        messages.success(request, '举报已提交，感谢你的反馈')

        if post_id:
            return redirect('posts:detail', pk=post_id)
        return redirect('posts:feed')

    return redirect('posts:feed')


@login_required
def unread_count_api(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})
