# Generated by Django 5.1.6 on 2025-04-09 00:48

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
                ('avg_time', models.FloatField(default=0)),
                ('branch', models.CharField(blank=True, max_length=25, null=True)),
                ('employee', models.CharField(blank=True, max_length=25, null=True)),
                ('state', models.CharField(default='None', max_length=25)),
                ('supplier', models.CharField(blank=True, max_length=25, null=True)),
                ('value', models.IntegerField(default=0)),
                ('estimated_delivery', models.DateTimeField(blank=True, null=True)),
                ('delivery', models.DateTimeField(blank=True, null=True)),
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
