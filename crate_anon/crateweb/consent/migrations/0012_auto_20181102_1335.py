# Generated by Django 2.1.2 on 2018-11-02 13:35

from django.db import migrations, models


"""
crate_anon/crateweb/consent/migrations/0010_auto_20180629_1238.py

===============================================================================

    Copyright (C) 2015-2018 Rudolf Cardinal (rudolf@pobox.com).

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

**Consent app, migration 0012.**

"""


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0011_auto_20181022_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamrep',
            name='team',
            field=models.CharField(max_length=100, unique=True, verbose_name='Team description'),  # noqa
        ),
    ]
