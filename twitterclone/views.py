from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
#from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from twitterclone.models import Tweet
from django.template import RequestContext, loader
from django.contrib.auth.models import User, Permission
import datetime
from twitterclone.models import UserPro, OtherProfile

"""def index(request):
	template = loader.get_template('twitterclone/index.html')
	my_user_list = User.objects.order_by('username')
	context = RequestContext(request, {
		'my_user_list':my_user_list
	})
	return HttpResponse(template.render(context))"""

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('twitterclone/login.html',c)



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
	tweeter = request.user
	dateandtime = datetime.datetime.now()
	t = Tweet(content=content,tweeter=tweeter,pub_date=dateandtime)
	t.save()
	return HttpResponseRedirect('/home')

def home(request):
	if request.user.is_authenticated():
		latest_tweet_list = Tweet.objects.order_by('-pub_date')[:5]
		template = loader.get_template('twitterclone/home.html')
		context = RequestContext(request, {'latest_tweet_list': latest_tweet_list,'username':request.user.username,})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect('/login')

def favorite(request,pk):
	my_tweet = Tweet.objects.get(pk=pk)
	my_tweet.favorites = my_tweet.favorites+1
	my_tweet.save()
	return HttpResponseRedirect('/home')

def profile(request,pk):

	my_user=User.objects.get(pk=pk)
	my_user_pro =UserPro.objects.get(username=my_user.username)
	my_other_pro=OtherProfile.objects.get(username=my_user.username)
	template = loader.get_template('twitterclone/profile.html')
	my_tweets = Tweet.objects.filter(tweeter=my_user)
	context = RequestContext(request, {'my_user':my_user,'following':my_user_pro.following,
		'followers':my_other_pro.userpro_set.all(),'my_tweets':my_tweets})
	return HttpResponse(template.render(context))
	#except:
	#	template = loader.get_template('twitterclone/profile.html')
	#	context = RequestContext(request, {'my_user':my_user,})

def my_profile(request):
	my_user = request.user
	my_user_pro =UserPro.objects.get(username=my_user.username)
	my_other_pro=OtherProfile.objects.get(username=my_user.username)
	template = loader.get_template('twitterclone/profile.html')
	my_tweets = Tweet.objects.filter(tweeter=my_user)
	context = RequestContext(request, {'my_user':my_user,'following':my_user_pro.following,
		'followers':my_other_pro.userpro_set.all(),'my_tweets':my_tweets})
	return HttpResponse(template.render(context))

	
def follow(request,pk):
	their_username = User.objects.get(pk=pk).username
	my_username = request.user.username
	me = UserPro.objects.get(username=my_username)
	himher = OtherProfile.objects.get(username=their_username)
	me.following = himher

	#my_name = me.following.username
	me.save()
	#me.following.add(himher)
	return HttpResponseRedirect('/home')
	#except:
		#return HttpResponseRedirect('/invalid')