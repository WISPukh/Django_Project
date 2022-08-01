# Generated by Django 4.0.5 on 2022-07-29 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('img_url', models.CharField(default=1659089253.5989192, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('price', models.IntegerField(default=0)),
                ('in_stock', models.IntegerField(default=0)),
                ('category', models.ManyToManyField(to='main.category')),
                ('content_type', models.ForeignKey(default=50, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Blender',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.product')),
                ('volume', models.IntegerField(default=1)),
                ('fan_speed', models.IntegerField(default=500)),
            ],
            bases=('main.product',),
        ),
        migrations.CreateModel(
            name='Combine',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.product')),
                ('volume', models.IntegerField(default=2)),
                ('max_power', models.IntegerField(default=50)),
            ],
            bases=('main.product',),
        ),
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.product')),
                ('height', models.IntegerField(default=100)),
                ('width', models.IntegerField(default=50)),
                ('length', models.IntegerField(default=60)),
            ],
            bases=('main.product',),
        ),
        migrations.CreateModel(
            name='Mixer',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.product')),
                ('mixer_type', models.CharField(max_length=50)),
                ('fan_speed', models.IntegerField(default=1000)),
                ('bowl_size', models.IntegerField(default=5)),
            ],
            bases=('main.product',),
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.product')),
                ('height', models.IntegerField(default=100)),
                ('width', models.IntegerField(default=50)),
                ('length', models.IntegerField(default=60)),
            ],
            bases=('main.product',),
        ),
        migrations.CreateModel(
            name='Teapot',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.product')),
                ('volume', models.IntegerField(default=2)),
                ('max_power', models.IntegerField(default=70)),
            ],
            bases=('main.product',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField(default=0)),
                ('total_quantity', models.IntegerField(default=0)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
    ]
