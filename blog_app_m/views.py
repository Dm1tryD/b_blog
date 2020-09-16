from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Post,Tag
from .utils import ObjectDetailMixin
from .forms import TagForm

def posts_list(request):
    posts = Post.objects.all()
    return render(request,'blog_app_m/index.html', context={'posts':posts})

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog_app_m/tags_list.html', context={'tags':tags})

class PostDetail(ObjectDetailMixin,View):
    model = Post
    template = 'blog_app_m/post_detail.html'

class TagDetail(ObjectDetailMixin,View):
    model = Tag
    template = 'blog_app_m/tag_detail.html'

class TagCreate(View):
    def get(self,request):
        form = TagForm()
        return render(request,'blog_app_m/tag_create.html',context={'form':form})
