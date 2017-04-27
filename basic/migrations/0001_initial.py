# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='InTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('comment', models.CharField(max_length=256)),
                ('date', models.DateTimeField(verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='OutTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('comment', models.CharField(max_length=256)),
                ('date', models.DateTimeField(verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Category')),
            ],
        ),
        migrations.AddField(
            model_name='outtransaction',
            name='sub_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.SubCategory'),
        ),
        migrations.AddField(
            model_name='intransaction',
            name='sub_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.SubCategory'),
        ),
    ]
