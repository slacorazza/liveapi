# Generated by Django 5.1.6 on 2025-02-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_activity_case_index_alter_activity_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('reference', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vendor', models.CharField(max_length=50)),
                ('pattern', models.CharField(choices=[('Similar Value', 'Similar Value'), ('Similar Reference', 'Similar Reference'), ('Exact Match', 'Exact Match'), ('Similar Date', 'Similar Date'), ('Similar Vendor', 'Similar Vendor'), ('Multiple', 'Multiple')], max_length=50)),
                ('open', models.BooleanField(default=True)),
                ('group_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Case',
        ),
    ]
