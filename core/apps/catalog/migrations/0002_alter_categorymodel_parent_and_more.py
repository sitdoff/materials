# Generated by Django 5.1.3 on 2024-11-13 11:13

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.categorymodel', verbose_name='Родительская категория'),
        ),
        migrations.AlterField(
            model_name='materialmodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='catalog.categorymodel', verbose_name='Категория'),
        ),
    ]
