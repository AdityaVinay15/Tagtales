# from urllib import request
# from django.shortcuts import render

# from post.models import Post

# def vblogs(request):
# 	posts = Post.objects.all()
#     return render(request, 'viewblogs.html',{'posts': posts})

from django.views.generic import ListView
from post.models import Post, Tag, Category

class PostListView(ListView):
    model = Post
    template_name = 'viewblogs.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-posted') 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.utils import timezone
@login_required
def create_blog(request):
    if request.method == 'POST':
        picture = request.FILES.get('picture')
        caption = request.POST.get('caption')
        category_name = request.POST.get('category')
        tags = request.POST.get('tags')

        if picture and caption and category_name and tags:
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            file_url = fs.url(filename)

            category, created = Category.objects.get_or_create(name=category_name)
            tag_list = []
            for tag in tags.split(','):
                tag_obj, created = Tag.objects.get_or_create(title=tag.strip())
                tag_list.append(tag_obj)

            post = Post.objects.create(
                user=request.user,
                picture=file_url,
                caption=caption,
                category=category,
                posted=timezone.now()
            )
            post.tags.set(tag_list)
            print("post successful")
            return redirect('main:landing')  # or wherever you want to redirect after successful post creation

    return render(request, 'createblog.html')