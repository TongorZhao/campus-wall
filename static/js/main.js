document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    document.querySelectorAll('[data-confirm]').forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});

function replyTo(commentId, authorName) {
    const input = document.getElementById('comment-input');
    if (input) {
        input.value = '@' + authorName + ' ';
        input.focus();
        input.scrollIntoView({ behavior: 'smooth' });
    }
}

function deleteComment(commentId) {
    if (confirm('确定要删除这条评论吗？')) {
        fetch('/posts/comment/' + commentId + '/delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            }
        }).then(response => {
            if (response.ok) {
                const element = document.getElementById('comment-' + commentId);
                if (element) {
                    element.remove();
                }
            }
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleLike(postId) {
    fetch('/posts/' + postId + '/like/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
        }
    }).then(response => response.json())
    .then(data => {
        const btn = document.querySelector('[data-post-id="' + postId + '"] .like-btn');
        const count = document.querySelector('[data-post-id="' + postId + '"] .like-count');
        if (btn) {
            btn.classList.toggle('liked', data.is_liked);
        }
        if (count) {
            count.textContent = data.like_count;
        }
    });
}

function checkUnreadNotifications() {
    fetch('/notifications/api/count/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            if (data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        }
    });
}

setInterval(checkUnreadNotifications, 60000);
