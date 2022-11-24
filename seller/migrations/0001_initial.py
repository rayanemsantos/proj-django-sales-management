# Generated by Django 4.1.3 on 2022-11-24 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, verbose_name='Telefone')),
            ],
            options={
                'verbose_name': 'vendedor',
                'verbose_name_plural': 'vendedores',
            },
        ),
    ]
