# Generated by Django 3.1.5 on 2021-01-28 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rm', '0026_auto_20210128_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interfacecall',
            name='interface_definition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interface_calls', to='rm.interfacedefinition'),
        ),
    ]
