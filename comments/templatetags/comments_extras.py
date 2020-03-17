from django import template
from ..forms import CommentForm
from blog.models import Post
from ..models import Comment

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time')
    # 等价于 comments_list = Comment.objects.filter(post=post).order_by('-created_time')

    comment_count = comment_list.count()

    return {
        'comment_list': comment_list,
        'comment_count': comment_count
    }
