from django.conf.urls import patterns, include, url

from django.contrib import admin
from twitterclone import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twitterclone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth_view'),
    url(r'^loggedin/$', views.loggedin, name='loggedin'),
    url(r'^invalid/$', views.invalid, name='invalid'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^make_tweet/$', views.make_tweet, name='make_tweet'),
    url(r'^get_tweet/$', views.get_tweet, name='get_tweet'),
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.login, name='login'),
    url(r'^(?P<pk>\d+)/favorite/$', views.favorite, name='favorite'),
    url(r'^(?P<pk>\d+)/profile/$', views.profile, name='profile'),
    url(r'^(?P<pk>\d+)/follow/n.*$', views.follow, name='follow'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^all_users/$', views.all_users, name='all_users'),
    url(r'^(?P<pk>\d+)/get_favorites/n.*$', views.get_favorites, name='get_favorites'),
    url(r'^already_faved/$', views.already_faved, name='already_faved'),





)
