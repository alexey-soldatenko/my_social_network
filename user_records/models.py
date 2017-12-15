from django.db import models
from auth_user.models import MyUser
from photo.models import UserPhoto
from django.conf import settings
import os

# Create your models here.
def delete_file(path):
	''' Удаление файла из файловой системы '''
	if os.path.isfile(path):
		os.remove(path)



def user_directory_path(instance, filename):
		return 'user_{0}/gallery/{1}'.format(instance.user.person_id, filename)

class UserRecord(models.Model):
	user = models.ForeignKey(MyUser, related_name='user')
	author_record = models.ForeignKey(MyUser, related_name='author')
	record_text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to=user_directory_path, blank=True)

	def save(self, *args, **kwargs):
		if self.image:
			photo = UserPhoto(user = self.user, photo = self.image)
			photo.save()
		super(UserRecord, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		if self.image:
			try:
				photo = UserPhoto.objects.get(user = self.user, photo = self.image)
				photo.delete()
			except UserPhoto.DoesNotExist:
				pass
			photo_name = self.image.url.split('/')[-1]
			path_to_file = os.path.join(settings.BASE_DIR, 'media/person/user_{0}/gallery/{1}').format(self.user.person_id, photo_name)
			delete_file(path_to_file)
		super(UserRecord, self).delete(*args, **kwargs)
	


class LikeRecord(models.Model):
	record_id = models.ForeignKey(UserRecord)
	author_record = models.ForeignKey(MyUser, related_name='author_record_for_like')
	user = models.ForeignKey(MyUser, related_name='user_like')
	date = models.DateTimeField(auto_now_add=True)

class RepostRecord(models.Model):
	record_id = models.ForeignKey(UserRecord)
	author_record = models.ForeignKey(MyUser, related_name='author_record_for_repost')
	user = models.ForeignKey(MyUser, related_name='user_repost')
	date = models.DateTimeField(auto_now_add=True)

class CommentRecord(models.Model):
	record_id = models.ForeignKey(UserRecord)
	author_record = models.ForeignKey(MyUser, related_name='author_record_for_comment')
	user = models.ForeignKey(MyUser, related_name='comment_user')
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
