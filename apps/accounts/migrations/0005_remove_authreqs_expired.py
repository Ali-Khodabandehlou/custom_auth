# Generated by Django 4.1.4 on 2022-12-28 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_authreqs_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authreqs',
            name='expired',
        ),
    ]
