from django.contrib import admin
from twitterclone.models import Tweet

class TweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['content']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Tweet, TweetAdmin)