# Generated by Django 5.1.7 on 2025-03-18 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_financialstatement_material_ui_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='financial_statement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classifications', to='budget.financialstatement'),
        ),
        migrations.AlterField(
            model_name='financialstatement',
            name='material_ui_icon',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Material UI icon'),
        ),
    ]
