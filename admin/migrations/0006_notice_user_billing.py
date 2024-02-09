# Generated by Django 5.0 on 2024-02-06 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='user',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=200)),
                ('amount', models.IntegerField(null=True)),
                ('remark', models.CharField(max_length=1000, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
