# Generated by Django 4.2.8 on 2023-12-31 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin", "0002_alter_user_managers_remove_user_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(default="unknown", max_length=10),
        ),
    ]
