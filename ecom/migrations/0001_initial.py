# Generated by Django 2.2.6 on 2019-11-16 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.BigIntegerField()),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
