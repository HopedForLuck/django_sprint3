from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).order_by('title')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category', 'location').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True),
        pk=id,
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.select_related().filter(
            slug=category_slug,
            is_published=True,
        )
    )
    post_list = Post.objects.filter(
        category=category, pub_date__lte=timezone.now(), is_published=True
    ).order_by('pub_date')
    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)
