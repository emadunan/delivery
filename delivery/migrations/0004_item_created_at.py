# Generated by Django 3.2 on 2021-05-04 18:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_item_unique_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
