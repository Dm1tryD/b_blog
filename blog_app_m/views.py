from django.shortcuts import render
from .models import Post
def posts_list(request):
    posts = Post.objects.all()
    return render(request,'blog_app_m/index.html', context={'posts':posts})


def post_detail(request,slug):
    post = Post.objects.get(slug__iexact=slug)
    return render(request, 'blog_app_m/post_detail.html',context={'post':post})
