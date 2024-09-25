
from django import forms

class BlogSearchForm(forms.Form):
    category = forms.CharField(required=False)
    customCategory = forms.CharField(required=False)
    query = forms.CharField(required=False)
    


# from django import forms
from post.models import Post, Category, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['picture', 'caption', 'category', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }