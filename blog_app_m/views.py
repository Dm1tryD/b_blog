from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Post,Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm,PostForm
from django.core.paginator import Paginator

def posts_list(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_page_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_page_url=''

    if page.has_next():
        next_page_url = '?page={}'.format(page.next_page_number())
    else:
        next_page_url=''

    context = {
        'page_obj': page,
        'is_paginated': is_paginated,
        'next_page_url': next_page_url,
        'prev_page_url':prev_page_url,
        'tags': tags
    }

    return render(request,'blog_app_m/index.html', context=context)

class PostDetail(ObjectDetailMixin,View):
    model = Post
    template = 'blog_app_m/post_detail.html'

class PostCreate(ObjectCreateMixin,View):
    model_form = PostForm
    template = 'blog_app_m/post_create.html'

class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog_app_m/post_update.html'

class PostDelete(ObjectDeleteMixin,View):
    model = Post
    template = 'blog_app_m/post_delete.html'
    redirect_url  = 'posts_list_url'

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog_app_m/tags_list.html', context={'tags':tags})

class TagDetail(ObjectDetailMixin,View):
    model = Tag
    template = 'blog_app_m/tag_detail.html'

class TagCreate(ObjectCreateMixin,View):
    model_form = TagForm
    template = 'blog_app_m/tag_create.html'

class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog_app_m/tag_update.html'

class TagDelete(ObjectDeleteMixin,View):
    model = Tag
    template = 'blog_app_m/tag_delete.html'
    redirect_url  = 'tags_list_url'