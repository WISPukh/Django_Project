# Generated by Django 4.0.5 on 2022-08-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_category_img_url_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='img_url',
            field=models.ImageField(default=1659598875.3173323, max_length=50, upload_to='category_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(default=1659598875.3135893, upload_to='uploads/'),
        ),
    ]
