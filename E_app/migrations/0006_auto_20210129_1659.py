# Generated by Django 3.0.3 on 2021-01-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_app', '0005_auto_20210129_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobile',
            name='battery_power',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='display_technology',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='ram',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='rom',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='screen_size',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='screen_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='weight',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]