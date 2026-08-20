# Generated manually for KYC document details fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_add_customer_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='aadhar_no',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='gst_no',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
        migrations.AddField(
            model_name='contact',
            name='pan_no',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='uin',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
