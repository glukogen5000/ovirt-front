# Generated by Django 3.2.10 on 2021-12-30 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_user_list_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_list',
            name='balanse',
            field=models.IntegerField(blank=True, null=True, verbose_name='Баланс'),
        ),
    ]
