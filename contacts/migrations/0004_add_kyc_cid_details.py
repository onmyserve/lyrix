# Generated manually for KYC CID details fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_add_kyc_document_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='bse_ucc',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='contact',
            name='ckyc_no',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='contact',
            name='lic_cid',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='contact',
            name='nse_ucc',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='contact',
            name='tnia_cid',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='contact',
            name='uiic_cid',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
