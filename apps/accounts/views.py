from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, FollowRelationship
from .forms import RegisterForm, ProfileEditForm
from apps.posts.models import Post


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！欢迎来到校园墙！')
            return redirect('posts:feed')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            next_url = request.GET.get('next', 'posts:feed')
            return redirect(next_url)
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, '已退出登录')
    return redirect('posts:feed')


@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'accounts/profile.html', {
        'profile_user': request.user,
        'posts': user_posts,
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料已更新')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile_user)
    is_following = False
    if request.user.is_authenticated:
        is_following = FollowRelationship.objects.filter(
            follower=request.user, following=profile_user
        ).exists()
    followers_count = FollowRelationship.objects.filter(following=profile_user).count()
    following_count = FollowRelationship.objects.filter(follower=profile_user).count()

    return render(request, 'accounts/user_profile.html', {
        'profile_user': profile_user,
        'posts': user_posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })


@login_required
def follow_toggle_view(request, username):
    if request.method == 'POST':
        target_user = get_object_or_404(User, username=username)
        if target_user == request.user:
            return JsonResponse({'error': '不能关注自己'}, status=400)

        relationship, created = FollowRelationship.objects.get_or_create(
            follower=request.user, following=target_user
        )
        if not created:
            relationship.delete()
            is_following = False
        else:
            is_following = True
            from apps.notifications.models import Notification
            Notification.objects.create(
                user=target_user,
                notification_type='follow',
                actor=request.user,
                message=f'{request.user.get_display_name()} 关注了你',
            )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_following': is_following,
                'followers_count': FollowRelationship.objects.filter(following=target_user).count(),
            })
        return redirect('accounts:user_profile', username=username)


@login_required
def followers_list_view(request):
    followers = FollowRelationship.objects.filter(following=request.user).select_related('follower')
    return render(request, 'accounts/follow_list.html', {
        'users': [f.follower for f in followers],
        'title': '我的粉丝',
    })


@login_required
def following_list_view(request):
    following = FollowRelationship.objects.filter(follower=request.user).select_related('following')
    return render(request, 'accounts/follow_list.html', {
        'users': [f.following for f in following],
        'title': '我的关注',
    })
