from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


class Tweet(models.Model):
	content = models.CharField(max_length=140)
	pub_date = models.DateTimeField('date published')
	def __unicode__(self):
		return self.content
	favorites=models.IntegerField(default=0)
	tweeter = models.CharField(max_length=20)
	def favorite(self):
		self.favorites = self.favorites+1;

class OtherProfile(models.Model):
	username = models.CharField(max_length=30,unique=True)
	def __unicode__(self):
		return self.username


class UserPro(models.Model):
	username = models.CharField(max_length=30)
	following = models.ForeignKey(OtherProfile,'username',blank=True,null=True)
	def __unicode__(self):
		return self.username


#class FavoriteClass(models.Model)
#	favedtweet = models.OneToOneField(Tweet, primary_key=True)
#	faving_user = models.ForeignKey(UserPro)