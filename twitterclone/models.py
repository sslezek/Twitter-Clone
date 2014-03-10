from django.db import models
from django.utils import timezone
import datetime

class Tweet(models.Model):
	content = models.CharField(max_length=140)
	pub_date = models.DateTimeField('date published')
	def __unicode__(self):
		return self.content
	favorites=models.IntegerField(default=0)
	tweeter = models.CharField(max_length=20)
