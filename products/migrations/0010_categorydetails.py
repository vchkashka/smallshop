# Generated by Django 4.2.1 on 2025-04-08 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('banner_image', models.ImageField(upload_to='')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='products.category')),
            ],
        ),
    ]
