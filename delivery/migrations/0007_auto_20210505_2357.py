# Generated by Django 3.1.7 on 2021-05-05 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_auto_20210505_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
