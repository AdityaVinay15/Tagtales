# from django.db import models

# from django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User
# from post.models import Post

from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.dispatch import receiver

# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
#     full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

#     if os.path.exists(full_path):
#     	os.remove(full_path)
# 	return profile_pic_name


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True, verbose_name='Picture')
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		SIZE = 250, 250

		if self.picture:
			pic = Image.open(self.picture.path)
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.picture.path)

	def __str__(self):
		return self.user.username
	
		
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)




from django.db import models
from django.contrib.auth.models import User
import random
import string

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def generate_otp_code(self):
        self.otp_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.save()
