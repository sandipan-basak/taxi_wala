# Generated by Django 3.1.6 on 2021-03-20 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_auto_20210315_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='travelled',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]