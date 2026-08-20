# Generated manually for Savings and Current Bank details fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_add_nominee_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='current_account_no',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='current_bank_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='current_ifsc_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='current_micr_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='savings_account_no',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='savings_bank_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='savings_ifsc_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='savings_micr_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
