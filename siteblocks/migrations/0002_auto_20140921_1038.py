# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteblocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='access_guest',
            field=models.BooleanField(default=False, help_text='Check it to grant access to this item to guests only.', db_index=True, verbose_name='Guests only'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='block',
            name='access_loggedin',
            field=models.BooleanField(default=False, help_text='Check it to grant access to this item to authenticated users only.', db_index=True, verbose_name='Logged in only'),
            preserve_default=True,
        ),
    ]
