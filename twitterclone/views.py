from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
#from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from twitterclone.models import Tweet
from django.template import RequestContext, loader
import datetime

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