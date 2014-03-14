# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Tweet.tweeter' to match new field type.
        db.rename_column(u'twitterclone_tweet', 'tweeter', 'tweeter_id')
        # Changing field 'Tweet.tweeter'
        db.alter_column(u'twitterclone_tweet', 'tweeter_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterclone.UserPro']))
        # Adding index on 'Tweet', fields ['tweeter']
        db.create_index(u'twitterclone_tweet', ['tweeter_id'])


    def backwards(self, orm):
        # Removing index on 'Tweet', fields ['tweeter']
        db.delete_index(u'twitterclone_tweet', ['tweeter_id'])


        # Renaming column for 'Tweet.tweeter' to match new field type.
        db.rename_column(u'twitterclone_tweet', 'tweeter_id', 'tweeter')
        # Changing field 'Tweet.tweeter'
        db.alter_column(u'twitterclone_tweet', 'tweeter', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'twitterclone.favoriteclass': {
            'Meta': {'object_name': 'FavoriteClass'},
            'faved_tweet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitterclone.Tweet']", 'null': 'True', 'blank': 'True'}),
            'faving_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitterclone.UserPro']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'twitterclone.otherprofile': {
            'Meta': {'object_name': 'OtherProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'twitterclone.retweet': {
            'Meta': {'object_name': 'Retweet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_tweet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitterclone.Tweet']", 'null': 'True', 'blank': 'True'}),
            'r_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitterclone.UserPro']", 'null': 'True', 'blank': 'True'})
        },
        u'twitterclone.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'favorites': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'tweeter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitterclone.UserPro']"})
        },
        u'twitterclone.userpro': {
            'Meta': {'object_name': 'UserPro'},
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['twitterclone.OtherProfile']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['twitterclone']