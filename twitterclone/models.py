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
	favoriteclass_set=[]
	def favorite(self):
		self.favorites = self.favorites+1;
	numfaves=len(favoriteclass_set)
	#rt = models.BooleanField(default=False)

class OtherProfile(models.Model):
	username = models.CharField(max_length=30,unique=True)
	def __unicode__(self):
		return self.username


class UserPro(models.Model):
	username = models.CharField(max_length=30)
	following = models.ManyToManyField(OtherProfile,'username',blank=True,null=True)
	def __unicode__(self):
		return self.username
	def get_following(self):
		list = []
		for use in self.following.all():
			list.append(use.username)
		return list


class FavoriteClass(models.Model):
	faved_tweet = models.ForeignKey(Tweet, blank=True,null=True)
	faving_user = models.ForeignKey(UserPro, blank=True,null=True)

class Retweet(models.Model):
	r_tweet = models.ForeignKey(Tweet, blank=True,null=True)
	r_user = models.ForeignKey(UserPro, blank=True,null=True)