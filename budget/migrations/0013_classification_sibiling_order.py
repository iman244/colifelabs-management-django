# Generated by Django 5.1.7 on 2025-03-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0012_alter_classification_financial_statement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='sibiling_order',
            field=models.SmallIntegerField(default=0, verbose_name='sibiling order'),
        ),
    ]
