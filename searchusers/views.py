from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .forms import ProfileSearchForm

def search_profiles(request):
    form = ProfileSearchForm(request.GET)
    profiles = User.objects.none()  # Initialize with an empty queryset

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            profiles = User.objects.filter(username__icontains=query)

    # For displaying default profiles when no query is provided
    if not query and profiles.count() == 0:
        profiles = User.objects.all()[:5]  # Show 5 default profiles

    return render(request, 'searchprofiles.html', {'form': form, 'profiles': profiles})


def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})
