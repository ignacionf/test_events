# Generated by Django 4.1.1 on 2022-09-07 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="capacity",
            field=models.PositiveSmallIntegerField(verbose_name="Max Capacity"),
        ),
        migrations.AlterField(
            model_name="room",
            name="name",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Room Name"
            ),
        ),
    ]
