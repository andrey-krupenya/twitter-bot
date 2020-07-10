# Generated by Django 3.0.8 on 2020-07-09 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_trafic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusFilterText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'Filter text status',
                'verbose_name_plural': 'Filters text status',
                'db_table': 'status_filter_text',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=45, unique=True)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45, unique=True)),
                ('password', models.CharField(max_length=45)),
                ('date', models.DateTimeField()),
                ('phone', models.CharField(max_length=21)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'Users',
                'managed': False,
            },
        ),
    ]