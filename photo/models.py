from django.db import models
from auth_user.models import MyUser

# Create your models here.
class UserPhoto(models.Model):
	user = models.ForeignKey(MyUser)
	photo = models.ImageField()
	date = models.DateTimeField(auto_now_add=True)