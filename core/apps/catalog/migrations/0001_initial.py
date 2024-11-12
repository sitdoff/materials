# Generated by Django 5.1.3 on 2024-11-12 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Код метериала')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость материала')),
            ],
        ),
    ]
