# Generated by Django 5.1.4 on 2024-12-15 03:45

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PullpayBE', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='description',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='church',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PullpayBE.church'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
