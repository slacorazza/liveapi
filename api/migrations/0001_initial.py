# Generated by Django 5.1.6 on 2025-03-20 10:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('insurance', models.IntegerField(default=0)),
                ('avg_time', models.FloatField(default=0)),
                ('type', models.CharField(default='None', max_length=25)),
                ('branch', models.CharField(default='None', max_length=25)),
                ('ramo', models.CharField(default='None', max_length=25)),
                ('brocker', models.CharField(default='None', max_length=25)),
                ('state', models.CharField(default='None', max_length=25)),
                ('client', models.CharField(default='None', max_length=25)),
                ('creator', models.CharField(default='None', max_length=25)),
                ('value', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('insurance_creation', models.DateTimeField()),
                ('insurance_start', models.DateTimeField()),
                ('insurance_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('activities', models.CharField(max_length=50)),
                ('cases', models.CharField(max_length=50)),
                ('number_cases', models.IntegerField(default=0)),
                ('percentage', models.FloatField(default=0)),
                ('avg_time', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('value', models.IntegerField(default=0)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='api.case')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('name', models.CharField(max_length=25)),
                ('case_index', models.IntegerField(default=0)),
                ('tpt', models.FloatField(default=0)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='api.case')),
            ],
        ),
        migrations.CreateModel(
            name='Rework',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cost', models.IntegerField(default=0)),
                ('target', models.CharField(default='None', max_length=250)),
                ('cause', models.CharField(default='None', max_length=250)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reworks', to='api.activity')),
            ],
        ),
    ]
