# Generated by Django 3.1.6 on 2021-03-20 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0003_ride_travelled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
