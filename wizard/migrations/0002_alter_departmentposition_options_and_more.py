# Generated by Django 4.2 on 2023-04-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentposition',
            options={'ordering': ['name'], 'verbose_name': 'Position', 'verbose_name_plural': 'Positions'},
        ),
        migrations.AlterField(
            model_name='mainskill',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
