from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
from django.conf import settings


# Create your models here.
class UserManager(BaseUserManager):
	#use_in_migrations = True

	def create_user(self, username, email, password, person_id):
		if not email:
			raise ValueError('Users must have an email address')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, person_id=person_id)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password, person_id):
		user = self.create_user(username=username, email=email, person_id=person_id, password=password)
		user.is_active = True
		user.is_staff = True
		user.is_superuser = True
		path_to_avatar = os.path.join(settings.MEDIA_URL, 'logo-img.png') 
		user.avatar = path_to_avatar
		user.save(using=self._db)
		return user

def user_directory_path(instance, filename):
		return 'user_{0}/avatar/{1}'.format(instance.person_id, filename)

class MyUser(AbstractBaseUser):
	id = models.AutoField(primary_key=True)
	person_id = models.PositiveIntegerField()
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=100)
	create_date = models.DateField(auto_now_add=True)
	last_visit = models.DateTimeField(auto_now=True)
	avatar = models.ImageField(upload_to=user_directory_path, blank=True)
	city = models.CharField(max_length=100, default='Неопределен')
	country = models.CharField(max_length=100, default='Неопределена')
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['person_id', 'username']

	objects = UserManager()

	def show_avatar(self):
		if self.avatar and hasattr(self.avatar, 'url'):
			return self.avatar.url

	def get_full_name(self):
		'''
        Returns the first_name plus the last_name, with a space in between.
        '''
		full_name = '%s' % (self.username)
		return full_name.strip()

	def get_short_name(self):
		'''
        Returns the short name for the user.
        '''
		return self.username

	def __str__(self):   
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

class MyFriends(models.Model):
	man = models.ForeignKey(MyUser, related_name='man')
	friend = models.ForeignKey(MyUser, related_name='friend')
	status = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ('man', 'friend')