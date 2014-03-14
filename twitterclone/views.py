from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
#from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext, loader
from django.contrib.auth.models import User, Permission
import datetime
from twitterclone.models import UserPro, OtherProfile, FavoriteClass,Tweet,Retweet
from django.contrib import messages

"""def index(request):
	template = loader.get_template('twitterclone/index.html')
	my_user_list = User.objects.order_by('username')
	context = RequestContext(request, {
		'my_user_list':my_user_list
	})
	return HttpResponse(template.render(context))"""

def login(request):
	if not UserPro.objects.all():
		new_user_pro = UserPro(username="admin")
		new_user_pro.save()
		new_other_profile = OtherProfile(username="admin")
		new_other_profile.save()

	c = {}
	c.update(csrf(request))
	return render_to_response('twitterclone/login.html',c)


def retweet(request,pk):
	my_tweet=Tweet.objects.get(pk=pk)
	my_user=request.user
	my_user_pro=my_user_pro =UserPro.objects.get(username=my_user.username)
	repeat = False
	if my_tweet.tweeter == my_user_pro:
		return HttpResponseRedirect('/rtself')
	for rtlol in my_tweet.retweet_set.all():
		that_user = rtlol.r_user
		if that_user == my_user_pro:
		    repeat = True
		    return HttpResponseRedirect('/already_rtd')
	if not repeat:
		newrt = Retweet(r_tweet=my_tweet,r_user=my_user_pro)
		my_tweet.retweets = my_tweet.retweets + 1
		my_tweet.save()
		newrt.save()
	else: HttpResponseRedirect('/already_rtd')
	return HttpResponseRedirect('/home')

def retweets(request,pk):
	my_user=request.user
	my_user_pro=UserPro.objects.get(username=my_user.username)
	my_tweet=Tweet.objects.get(pk=pk)
	rts=my_tweet.retweet_set.all()
	my_set= set()
	for rt in rts:
		user_lol = UserPro.objects.get(username=rt.r_user)
		my_set.add(user_lol)

	template = loader.get_template('twitterclone/retweets.html')
	context = RequestContext(request, {'rts':my_set})
	return HttpResponse(template.render(context))

def rtself(request):
	template = loader.get_template('twitterclone/rtself.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))


def get_favorites(request,pk):

	my_tweet=Tweet.objects.get(pk=pk)
	faves=my_tweet.favoriteclass_set.all()
	my_faves = set()
	for fave in faves:
		user_lol=UserPro.objects.get(username=fave.faving_user)
		my_faves.add(user_lol)
	template = loader.get_template('twitterclone/get_favorites.html')
	context = RequestContext(request, {'faves':my_faves})
	return HttpResponse(template.render(context))

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		user.save()
		has_profile=-5
		try:
			has_profile = UserPro.objects.get(username=username)
		except:	
			error=1
		if has_profile == -5:
			new_user_pro = UserPro(username=username)
			new_user_pro.save()
			new_other_profile = OtherProfile(username=username)
			new_other_profile.save()
		return HttpResponseRedirect('/home')
	else:
		return HttpResponseRedirect('/invalid')

def loggedin(request):
	return render_to_response('twitterclone/loggedin.html',
							  {'username': request.user.username})

def invalid(request):
	return render_to_response('twitterclone/invalid.html')

def logout(request):
	auth.logout(request)
	return render_to_response('twitterclone/logout.html')

def register_user(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/register_success')

	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	return render_to_response('twitterclone/register.html',args)

def register_success(request):
	return render_to_response('twitterclone/register_success.html')

def get_tweet(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('twitterclone/get_tweet.html',c)
	
def make_tweet(request):
	content = request.POST.get('content', '')
	my_user=request.user
	my_user_pro=UserPro.objects.get(username=my_user.username)
	dateandtime = datetime.datetime.now()
	t = Tweet(content=content,tweeter=my_user_pro,pub_date=dateandtime)
	t.save()
	return HttpResponseRedirect('/home')

def home(request):
	if request.user.is_authenticated():
		my_user=request.user
		my_user_pro=UserPro.objects.get(username=my_user.username)
		my_following_list = my_user_pro.get_following()
		folo_list_two = set()
		for foloing in my_following_list:
			new_folo = UserPro.objects.get(username=foloing)
			folo_list_two.add(new_folo)
		all_tweets = set()
		for lol_tweet in Tweet.objects.filter(tweeter__in=folo_list_two):
			all_tweets.add(lol_tweet)
		for tweet in Tweet.objects.all():
			tweet.is_rt = False
			breakk = False
			for a_tweet in all_tweets:
				if a_tweet == tweet:
					breakk = True
			if not breakk:
				for follo in folo_list_two:
					for retweetable in tweet.retweet_set.all():
						if not breakk:
							if retweetable.r_user == follo:
								tweet.is_rt = True
								tweet.retweeter = follo.username
								all_tweets.add(tweet)
								breakk=True
		#latest_tweet_list = all_tweets.order_by('-pub_date')[:5]
		template = loader.get_template('twitterclone/home.html')
		context = RequestContext(request, {'latest_tweet_list': all_tweets,'username':request.user.username,})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect('/login')

def favorite(request,pk):
	my_user=request.user
	my_user_pro=UserPro.objects.get(username=my_user.username)
	my_tweet = Tweet.objects.get(pk=pk)
	the_fave = FavoriteClass()
	the_fave.save()
	repeat = False
	for favelol in my_tweet.favoriteclass_set.all():
		that_user = favelol.faving_user
		if that_user == my_user_pro:
		    repeat = True
		    return HttpResponseRedirect('/already_faved')

	if not repeat:
		my_tweet.favoriteclass_set.add(the_fave)
		my_user_pro.favoriteclass_set.add(the_fave)
		my_tweet.favorites = my_tweet.favorites+1
	the_fave.save()
	my_tweet.save()
	return HttpResponseRedirect('/home')

def all_users(request):
	user_list = UserPro.objects.all()
	my_user=request.user
	my_user_pro=UserPro.objects.get(username=my_user.username)
	my_following_list = my_user_pro.get_following()
	not_following = user_list.exclude(username__in=my_following_list)
	following_list = user_list.filter(username__in=my_following_list)
	template=loader.get_template('twitterclone/all_users.html')
	context = RequestContext(request, {'user_list':not_following,'second_list':following_list})
	return HttpResponse(template.render(context))

def profile(request,pk):

	my_user=User.objects.get(pk=pk)
	my_user_pro =UserPro.objects.get(username=my_user.username)
	my_other_pro=OtherProfile.objects.get(username=my_user.username)
	template = loader.get_template('twitterclone/profile.html')
	my_tweets = Tweet.objects.filter(tweeter=my_user_pro)
	my_rts = set()
	for tweet in Tweet.objects.all():
		for retweetlol in tweet.retweet_set.all():
			if retweetlol.r_user == my_user_pro:
				my_rts.add(tweet)
	context = RequestContext(request, {'my_user':my_user,'following':my_user_pro.following.all(),
		'followers':my_other_pro.userpro_set.all(),'my_tweets':my_tweets,'my_rts':my_rts})
	return HttpResponse(template.render(context))
	#except:
	#	template = loader.get_template('twitterclone/profile.html')
	#	context = RequestContext(request, {'my_user':my_user,})

def my_profile(request):
	my_user = request.user
	my_user_pro =UserPro.objects.get(username=my_user.username)
	my_other_pro=OtherProfile.objects.get(username=my_user.username)
	template = loader.get_template('twitterclone/profile.html')
	my_tweets = Tweet.objects.filter(tweeter=my_user_pro)
	my_rts = set()
	for tweet in Tweet.objects.all():
		for retweetlol in tweet.retweet_set.all():
			if retweetlol.r_user == my_user_pro:
				my_rts.add(tweet)
	context = RequestContext(request, {'my_user':my_user,'following':my_user_pro.following.all(),
		'followers':my_other_pro.userpro_set.all(),'my_tweets':my_tweets,'my_rts':my_rts})
	return HttpResponse(template.render(context))

	
def follow(request,pk):
	their_username = User.objects.get(pk=pk).username
	my_username = request.user.username
	me = UserPro.objects.get(username=my_username)
	himher = OtherProfile.objects.get(username=their_username)
	me.following.add(himher)

	#my_name = me.following.username
	me.save()
	#me.following.add(himher)
	return HttpResponseRedirect('/home')
	#except:
		#return HttpResponseRedirect('/invalid')

def already_faved(request):
	template = loader.get_template('twitterclone/already_faved.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def already_rtd(request):
	template = loader.get_template('twitterclone/already_rtd.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
"""
f=FavoriteClass()
f.save()
my_tweet=Tweet(content="hi",tweeter="sam")
my_tweet.save()
my_user = UserPro(username="sdotslezek")
my_user.save()
f.faving_user=my_user
f.faved_tweet=my_tweet
f.save()
my_set = my_tweet.favoriteclass_set.all()
"""