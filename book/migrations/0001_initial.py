# Generated by Django 5.0.1 on 2024-02-28 19:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_name', models.CharField(max_length=255)),
                ('author_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('genre', models.CharField(max_length=100)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/')),
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('administrator_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administrator_username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('mobile', models.TextField(default='', max_length=10)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='book.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unitcost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('orderid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='book.order')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_order', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('shopping_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_details', to='book.shoppingcart')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.customer')),
            ],
        ),
    ]
