# Generated by Django 5.0.1 on 2024-03-02 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='orderid',
            new_name='order_id',
        ),
    ]
