from django.contrib import admin
from post.models import Post,Tag,Follow,Category,Stream
# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Category)
admin.site.register(Stream)