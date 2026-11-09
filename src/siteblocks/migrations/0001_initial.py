# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(help_text='Short name to address this block from a template.', max_length=80, verbose_name='Alias', db_index=True)),
                ('description', models.CharField(help_text='Short memo for this block.', max_length=100, null=True, verbose_name='Description', blank=True)),
                ('url', models.CharField(help_text='Page URL this block is related to. Regular expressions supported (e.g.: "/news.*" &#8212; everything under "/news").<br />View names are supported: prepend <b>:</b> to view name <br /><b>Reserved URL alias:</b> "*" &#8212; every page.', max_length=200, verbose_name='URL')),
                ('contents', models.TextField(help_text='Block contents to render in a template.', verbose_name='Contents')),
                ('hidden', models.BooleanField(default=False, help_text='Whether to show this block when requested.', db_index=True, verbose_name='Hidden')),
            ],
            options={
                'verbose_name': 'Site Block',
                'verbose_name_plural': 'Site Blocks',
            },
            bases=(models.Model,),
        ),
    ]
