# Generated by Django 4.0.3 on 2022-03-18 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prod_ord', '0003_rename_prise_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='prod_ord.staff'),
        ),
    ]