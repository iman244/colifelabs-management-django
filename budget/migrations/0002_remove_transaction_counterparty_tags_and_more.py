# Generated by Django 5.1.7 on 2025-03-11 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
        ('ecosystem', '0002_counterpartytag_counterparty_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='counterparty_tags',
        ),
        migrations.AddField(
            model_name='transaction',
            name='counterparty_tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='ecosystem.counterpartytag'),
            preserve_default=False,
        ),
    ]
