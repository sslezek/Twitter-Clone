from django.contrib import admin
from twitterclone.models import Tweet, UserPro, OtherProfile

class TweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['content']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Tweet, TweetAdmin)

class UserProAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username']}),
		('following', {'fields':['following']}),
	]

admin.site.register(UserPro,UserProAdmin)

class OtherProfileAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username']}),
	]

admin.site.register(OtherProfile,OtherProfileAdmin)