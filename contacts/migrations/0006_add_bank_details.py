# Generated manually for Bank details fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_add_address_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='account_no',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='bank_account_type',
            field=models.CharField(blank=True, default='Savings Account', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='bank_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='ifsc_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='micr_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
