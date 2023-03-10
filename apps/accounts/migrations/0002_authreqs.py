# Generated by Django 4.1.4 on 2022-12-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthReqs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=16)),
                ('status', models.CharField(choices=[('requested', 'requested'), ('success', 'success'), ('failed', 'failed')], max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('expired', models.BooleanField(default=False)),
            ],
        ),
    ]
