# Generated by Django 3.2 on 2021-05-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_item_avaliability'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='item',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_name'),
        ),
    ]
