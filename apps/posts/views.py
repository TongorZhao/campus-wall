from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.utils.text import slugify
from django.conf import settings
from django.views.decorators.http import require_POST
from .models import Post, Category, Tag, Like, Comment, CommentLike, Favorite, PostImage
from .forms import PostForm, PostImageFormSet, CommentForm, SearchForm
from apps.notifications.models import Notification


def feed_view(request):
    posts = Post.objects.filter(is_deleted=False).select_related(
        'author', 'category'
    ).prefetch_related('tags', 'images')

    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    sort = request.GET.get('sort', 'newest')
    if sort == 'hot':
        posts = posts.order_by('-is_pinned', '-like_count', '-comment_count', '-created_at')
    else:
        posts = posts.order_by('-is_pinned', '-created_at')

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)
    search_form = SearchForm()

    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))
    else:
        liked_post_ids = set()
        favorited_post_ids = set()

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'categories': categories,
        'search_form': search_form,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
        'current_sort': sort,
        'current_category': category_slug,
    })


def hot_view(request):
    posts = Post.objects.filter(is_deleted=False).select_related(
        'author', 'category'
    ).prefetch_related('tags', 'images').order_by('-is_pinned', '-like_count', '-comment_count', '-created_at')

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)

    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))
    else:
        liked_post_ids = set()
        favorited_post_ids = set()

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'categories': categories,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
        'current_sort': 'hot',
        'page_title': '热门帖子',
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    posts = Post.objects.filter(is_deleted=False, category=category).select_related(
        'author', 'category'
    ).prefetch_related('tags', 'images').order_by('-is_pinned', '-created_at')

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)

    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))
    else:
        liked_post_ids = set()
        favorited_post_ids = set()

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'categories': categories,
        'current_category': category.slug,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
    })


def tag_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(is_deleted=False, tags=tag).select_related(
        'author', 'category'
    ).prefetch_related('tags', 'images').order_by('-created_at')

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)

    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))
    else:
        liked_post_ids = set()
        favorited_post_ids = set()

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'categories': categories,
        'current_tag': tag,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
    })


def search_view(request):
    form = SearchForm(request.GET)
    posts = Post.objects.none()
    query = ''

    if form.is_valid():
        query = form.cleaned_data['q']
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_deleted=False,
        ).select_related('author', 'category').prefetch_related('tags', 'images')

        category = form.cleaned_data.get('category')
        if category:
            posts = posts.filter(category__slug=category)

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)

    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))
    else:
        liked_post_ids = set()
        favorited_post_ids = set()

    return render(request, 'posts/search.html', {
        'posts': posts,
        'query': query,
        'form': form,
        'categories': categories,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
    })


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        formset = PostImageFormSet(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag_slug = slugify(tag_name, allow_unicode=True)
                    tag, _ = Tag.objects.get_or_create(
                        slug=tag_slug,
                        defaults={'name': tag_name}
                    )
                    post.tags.add(tag)

            formset = PostImageFormSet(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
            else:
                for form in formset:
                    for error in form.errors.values():
                        messages.error(request, f'图片上传失败: {error}')

            messages.success(request, '帖子发布成功！')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
        formset = PostImageFormSet()

    categories = Category.objects.filter(is_active=True)
    return render(request, 'posts/create.html', {
        'form': form,
        'formset': formset,
        'categories': categories,
    })


def post_detail_view(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags', 'images'),
        pk=pk,
        is_deleted=False,
    )

    if request.user.is_authenticated and post.author != request.user:
        Post.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
        post.refresh_from_db()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = form.cleaned_data.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id, post=post, is_deleted=False)
                comment.parent = parent_comment
            comment.save()
            Post.objects.filter(pk=pk).update(comment_count=F('comment_count') + 1)
            if post.author != request.user:
                notification_type = 'reply' if parent_id else 'comment'
                Notification.objects.create(
                    user=post.author,
                    notification_type=notification_type,
                    actor=request.user,
                    post=post,
                    message=f'{request.user.get_display_name()} 评论了你的帖子「{post.title}」',
                )
            messages.success(request, '评论发表成功！')
            return redirect('posts:detail', pk=pk)

    comments = post.comments.filter(is_deleted=False).select_related('author').prefetch_related('replies__author')

    top_level_comments = comments.filter(parent=None)
    comment_form = CommentForm()

    is_liked = False
    is_favorited = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
        is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()

    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': top_level_comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'is_favorited': is_favorited,
    })


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            tags_input = form.cleaned_data.get('tags_input', '')
            post.tags.clear()
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag_slug = slugify(tag_name, allow_unicode=True)
                    tag, _ = Tag.objects.get_or_create(
                        slug=tag_slug,
                        defaults={'name': tag_name}
                    )
                    post.tags.add(tag)

            formset = PostImageFormSet(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()

            messages.success(request, '帖子已更新！')
            return redirect('posts:detail', pk=post.pk)
        tags_input = form.cleaned_data.get('tags_input', '')
    else:
        initial_tags = ', '.join(post.tags.values_list('name', flat=True))
        form = PostForm(instance=post, initial={'tags_input': initial_tags})
        formset = PostImageFormSet(instance=post)
        tags_input = initial_tags

    categories = Category.objects.filter(is_active=True)
    return render(request, 'posts/edit.html', {
        'form': form,
        'formset': formset,
        'post': post,
        'categories': categories,
        'tags_input': tags_input,
    })


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author and not request.user.is_staff:
        messages.error(request, '你没有权限删除这篇帖子')
        return redirect('posts:detail', pk=pk)

    if request.method == 'POST':
        post.soft_delete()
        messages.success(request, '帖子已删除')
        return redirect('posts:feed')

    return render(request, 'posts/delete_confirm.html', {'post': post})


@login_required
def post_like_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': '无效请求'}, status=400)

    post = get_object_or_404(Post, pk=pk, is_deleted=False)

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        is_liked = False
        Post.objects.filter(pk=pk, like_count__gt=0).update(like_count=F('like_count') - 1)
    else:
        is_liked = True
        Post.objects.filter(pk=pk).update(like_count=F('like_count') + 1)
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                notification_type='like',
                actor=request.user,
                post=post,
                message=f'{request.user.get_display_name()} 赞了你的帖子「{post.title}」',
            )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post.refresh_from_db()
        return JsonResponse({
            'is_liked': is_liked,
            'like_count': post.like_count,
        })

    return redirect('posts:detail', pk=pk)


@login_required
def post_favorite_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': '无效请求'}, status=400)

    post = get_object_or_404(Post, pk=pk, is_deleted=False)

    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorited': is_favorited})

    return redirect('posts:detail', pk=pk)


@login_required
def my_favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'post', 'post__author', 'post__category'
    ).prefetch_related('post__tags', 'post__images')
    posts = [fav.post for fav in favorites]

    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))

    return render(request, 'posts/my_favorites.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
    })


@login_required
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user, is_deleted=False).select_related(
        'author', 'category'
    ).prefetch_related('tags', 'images')

    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    favorited_post_ids = set(Favorite.objects.filter(user=request.user).values_list('post_id', flat=True))

    return render(request, 'posts/my_posts.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'favorited_post_ids': favorited_post_ids,
    })


@login_required
@require_POST
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user, is_deleted=False)
    post = comment.post
    comment.soft_delete()
    Post.objects.filter(pk=post.pk, comment_count__gt=0).update(comment_count=F('comment_count') - 1)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('posts:detail', pk=post.pk)
