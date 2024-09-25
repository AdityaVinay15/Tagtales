import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.utils.text import slugify
from django.urls import reverse

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
	title = models.CharField(max_length=75, verbose_name='Tag')
	#to generate urls with title name
	slug = models.SlugField(null=False, unique=True)

	class Meta:
		verbose_name='Tag'
		verbose_name_plural = 'Tags'

	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])
		
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)

class PostFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
	file = models.FileField(upload_to=user_directory_path)

class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	# content =  models.ManyToManyField(PostFileContent, related_name='contents')
	picture=models.ImageField(upload_to=user_directory_path,verbose_name='Picture',default='Tagtales\static\images\hashtag.png')
	caption = models.TextField(max_length=2000, verbose_name='Caption')
	posted = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, related_name='tags')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')


	def get_absolute_url(self):
		return reverse('postdetails', args=[str(self.id)])

	def __str__(self):
		return str(self.id)
	
#reltnship between users
class Follow(models.Model):
	follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
	following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')
	
	
#after posting anything it will be pushed to all your followers
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
    	post = instance
    	user = post.user
		#instance of people who all are following you
    	followers = Follow.objects.all().filter(following=user)
		#pushing the posts to following people
    	for follower in followers:
    		stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
    		stream.save()
post_save.connect(Stream.add_post, sender=Post)
# post_save.connect(Likes.user_liked_post, sender=Likes)
# post_delete.connect(Likes.user_unlike_post, sender=Likes)

#Follow
# post_save.connect(Follow.user_follow, sender=Follow)
# post_delete.connect(Follow.user_unfollow, sender=Follow)