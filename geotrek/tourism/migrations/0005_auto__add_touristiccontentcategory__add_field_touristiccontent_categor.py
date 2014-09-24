# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TouristicContentCategory'
        db.create_table('t_b_touristic_content', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=512, null=True, db_column='picto')),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128, db_column='nom')),
        ))
        db.send_create_signal(u'tourism', ['TouristicContentCategory'])

        # Adding field 'TouristicContent.category'
        db.add_column('t_t_touristic_content', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='contents', db_column='category', to=orm['tourism.TouristicContentCategory']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'TouristicContentCategory'
        db.delete_table('t_b_touristic_content')

        # Deleting field 'TouristicContent.category'
        db.delete_column('t_t_touristic_content', 'category')


    models = {
        u'authent.structure': {
            'Meta': {'ordering': "['name']", 'object_name': 'Structure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'tourism.datasource': {
            'Meta': {'ordering': "['title', 'url']", 'object_name': 'DataSource', 'db_table': "'t_t_source_donnees'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '512', 'db_column': "'picto'"}),
            'targets': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'titre'"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'type'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400', 'db_column': "'url'"})
        },
        u'tourism.touristiccontent': {
            'Meta': {'object_name': 'TouristicContent', 'db_table': "'t_t_touristic_content'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'db_column': "'category'", 'to': u"orm['tourism.TouristicContentCategory']"}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'date_insert'", 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'date_update'", 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'supprime'"}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '2154'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'nom'"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authent.Structure']", 'db_column': "'structure'"})
        },
        u'tourism.touristiccontentcategory': {
            'Meta': {'ordering': "['label']", 'object_name': 'TouristicContentCategory', 'db_table': "'t_b_touristic_content'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'nom'"}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '512', 'null': 'True', 'db_column': "'picto'"})
        }
    }

    complete_apps = ['tourism']