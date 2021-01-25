# Generated by Django 3.1.5 on 2021-01-25 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210115_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='cost_centre',
            field=models.CharField(default='<<onbekend>>', max_length=50, verbose_name='Kostenplaats'),
        ),
        migrations.AddField(
            model_name='department',
            name='cost_centre',
            field=models.CharField(default='<<onbekend>>', max_length=50, verbose_name='Kostenplaats'),
        ),
        migrations.AddField(
            model_name='team',
            name='cost_centre',
            field=models.CharField(default='<<onbekend>>', max_length=50, verbose_name='Kostenplaats'),
        ),
    ]
