# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.utils.timezone
import djangocms_text_ckeditor.fields
from django.conf import settings
import app_data.fields
import cms.models.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('filer', '0002_auto_20150606_2003'),
        ('cms', '0003_auto_20140926_2347'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name='Ordering')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(help_text='Auto-generated. Clean it to have it re-created. WARNING! Used in the URL. If changed, the URL will change. ', max_length=255, verbose_name='Slug', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_blog.Category', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'aldryn_blog_category_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('latest_entries', models.IntegerField(default=5, help_text='The number of latests entries to be displayed.')),
                ('tags', models.ManyToManyField(help_text='Show only the blog posts tagged with chosen tags.', to='taggit.Tag', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, blank=True, help_text='Used in the URL. If changed, the URL will change. Clean it to have it re-created.', unique=True, verbose_name='Slug')),
                ('language', models.CharField(choices=[(b'es', 'Spanish'), (b'en', 'English')], max_length=5, blank=True, help_text='leave empty to display in all languages', null=True, verbose_name='language')),
                ('lead_in', djangocms_text_ckeditor.fields.HTMLField(help_text='Will be displayed in lists, and at the start of the detail page (in bold)', verbose_name='Lead-in')),
                ('publication_start', models.DateTimeField(default=django.utils.timezone.now, help_text='Used in the URL. If changed, the URL will change.', verbose_name='Published Since')),
                ('publication_end', models.DateTimeField(null=True, verbose_name='Published Until', blank=True)),
                ('app_data', app_data.fields.AppDataField(default=b'{}', editable=False)),
                ('author', models.ForeignKey(verbose_name='Author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='aldryn_blog.Category', null=True)),
                ('coauthors', models.ManyToManyField(related_name='aldryn_blog_coauthors', null=True, verbose_name='Co-Authors', to=settings.AUTH_USER_MODEL, blank=True)),
                ('content', cms.models.fields.PlaceholderField(related_name='aldryn_blog_posts', slotname=b'aldryn_blog_post_content', editable=False, to='cms.Placeholder', null=True)),
                ('key_visual', filer.fields.image.FilerImageField(verbose_name='Key Visual', blank=True, to='filer.Image', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['-publication_start'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
    ]
