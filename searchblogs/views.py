from django.shortcuts import redirect, render
from post.models import Post
from searchblogs.forms import BlogSearchForm, PostForm
from django.contrib.auth.decorators import login_required
def search_form(request):
    form = BlogSearchForm()
    return render(request, 'searchblogs.html', {'form': form})


def search_results(request):
    if request.method == 'GET':
        form = BlogSearchForm(request.GET)
        results = Post.objects.none()

        if form.is_valid():
            category = form.cleaned_data.get('category')
            custom_category = form.cleaned_data.get('customCategory')
            query = form.cleaned_data.get('query')

            print(f"Category: {category}")
            print(f"Custom Category: {custom_category}")
            print(f"Query: {query}")

            # Use custom_category if provided, else use category
            filter_category = custom_category if custom_category else category

            if filter_category:
                results = Post.objects.filter(category__name__icontains=filter_category)
                print(f"Results after category filter: {results}")

            if query:
                # Filter by caption
                caption_results = results.filter(caption__icontains=query)
                print(f"Caption Filter Results: {caption_results}")

                # Filter by tags
                tag_results = Post.objects.filter(tags__title__icontains=query)
                print(f"Tag Filter Results: {tag_results}")

                # Combine results
                if caption_results.exists() or tag_results.exists():
                    results = caption_results | tag_results
                else:
                    # If no tags match, use only category filter
                    results = Post.objects.filter(category__name__icontains=filter_category)
                print(f"Results after combining filters: {results}")

        else:
            print("Form is not valid")

    else:
        form = BlogSearchForm()

    return render(request, 'searchblogsresults.html', {'form': form, 'results': results})

def createpost(request):
    return render(request,'createblog.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('viewblogs:view')  # Redirect to the list of posts or the post detail page
    else:
        form = PostForm()
    return render(request, 'createblog.html', {'form': form})


