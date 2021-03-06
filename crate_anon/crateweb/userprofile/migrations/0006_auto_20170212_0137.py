#!/usr/bin/env python

"""
crate_anon/crateweb/userprofile/migrations/0006_auto_20170212_0137.py

===============================================================================

    Copyright (C) 2015-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

**Userprofile app, migration 0006.**

"""
# Generated by Django 1.10.5 on 2017-02-12 01:37
from __future__ import unicode_literals

from cardinal_pythonlib.django.fields.jsonclassfield import JsonClassField
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_userprofile_patient_multiquery_scratchpad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='patient_multiquery_scratchpad',
            field=JsonClassField(null=True, verbose_name='PatientMultiQuery scratchpad (in JSON) for builder'),  # noqa
        ),
    ]
