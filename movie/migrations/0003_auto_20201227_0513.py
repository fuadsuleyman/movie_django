# Generated by Django 3.1.4 on 2020-12-27 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_actor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Name'),
        ),
    ]
