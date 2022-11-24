# Generated by Django 4.1.3 on 2022-11-24 01:38

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(db_index=True, unique=True, verbose_name='Código')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True, verbose_name='Preço unitário')),
                ('commission_percentage', models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[product.models.validate_commission_percentage], verbose_name='Porcentagem de comissão')),
            ],
            options={
                'verbose_name': 'produto',
                'verbose_name_plural': 'produtos',
            },
        ),
    ]