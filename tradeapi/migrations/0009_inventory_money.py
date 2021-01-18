# Generated by Django 3.1.2 on 2021-01-18 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeapi', '0008_auto_20210118_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='money',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=7),
            preserve_default=False,
        ),
    ]
