# Generated by Django 2.1.3 on 2018-11-12 08:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('birth', models.DateField(blank=True, null=True)),
                ('former_names', models.CharField(max_length=100)),
                ('identifiers', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=70, unique=True)),
                ('councilor_terms', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('election_year', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('party', models.CharField(max_length=100, null=True)),
                ('constituency', models.IntegerField()),
                ('county', models.CharField(max_length=100)),
                ('district', models.TextField()),
                ('votes', models.IntegerField()),
                ('votes_percentage', models.CharField(max_length=100)),
                ('elected', models.BooleanField()),
                ('contact_details', django.contrib.postgres.fields.jsonb.JSONField()),
                ('education', models.TextField()),
                ('experience', models.TextField()),
                ('remark', models.TextField()),
                ('image', models.CharField(max_length=200)),
                ('links', django.contrib.postgres.fields.jsonb.JSONField()),
                ('platform', models.TextField()),
                ('politicalcontributions', django.contrib.postgres.fields.jsonb.JSONField()),
                ('elected_councilor_id', models.IntegerField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('type', models.CharField(max_length=20)),
                ('votes_detail', django.contrib.postgres.fields.jsonb.JSONField()),
                ('occupy', models.BooleanField()),
                ('status', models.CharField(max_length=100)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='candidates.Candidates', to_field='uid')),
            ],
        ),
    ]
