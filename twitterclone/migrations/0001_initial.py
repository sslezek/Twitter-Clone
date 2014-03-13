# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tweet'
        db.create_table(u'twitterclone_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('favorites', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tweeter', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'twitterclone', ['Tweet'])

        # Adding model 'OtherProfile'
        db.create_table(u'twitterclone_otherprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'twitterclone', ['OtherProfile'])

        # Adding model 'UserPro'
        db.create_table(u'twitterclone_userpro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'twitterclone', ['UserPro'])

        # Adding M2M table for field following on 'UserPro'
        m2m_table_name = db.shorten_name(u'twitterclone_userpro_following')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userpro', models.ForeignKey(orm[u'twitterclone.userpro'], null=False)),
            ('otherprofile', models.ForeignKey(orm[u'twitterclone.otherprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userpro_id', 'otherprofile_id'])

        # Adding model 'FavoriteClass'
        db.create_table(u'twitterclone_favoriteclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('faved_tweet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterclone.Tweet'], null=True, blank=True)),
            ('faving_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterclone.UserPro'], null=True, blank=True)),
        ))
        db.send_create_signal(u'twitterclone', ['FavoriteClass'])

        # Adding model 'Retweet'
        db.create_table(u'twitterclone_retweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('r_tweet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterclone.Tweet'], null=True, blank=True)),
            ('r_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterclone.UserPro'], null=True, blank=True)),
        ))
        db.send_create_signal(u'twitterclone', ['Retweet'])


    def backwards(self, orm):
        # Deleting model 'Tweet'
        db.delete_table(u'twitterclone_tweet')

        # Deleting model 'OtherProfile'
        db.delete_table(u'twitterclone_otherprofile')

        # Deleting model 'UserPro'
        db.delete_table(u'twitterclone_userpro')

        # Removing M2M table for field following on 'UserPro'
        db.delete_table(db.shorten_name(u'twitterclone_userpro_following'))

        # Deleting model 'FavoriteClass'
        db.delete_table(u'twitterclone_favoriteclass')

        # Deleting model 'Retweet'
        db.delete_table(u'twitterclone_retweet')


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
            'tweeter': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'twitterclone.userpro': {
            'Meta': {'object_name': 'UserPro'},
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['twitterclone.OtherProfile']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['twitterclone']