# Generated manually for Mandate details fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_add_family_details_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='bse_mandate_bank',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='bse_mandate_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='bse_mandate_limit',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='bse_mandate_payer',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='bse_mandate_umrn',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='cams_mandate_bank',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='cams_mandate_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='cams_mandate_limit',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='cams_mandate_payer',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='cams_mandate_umrn',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='kfin_mandate_bank',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='kfin_mandate_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='kfin_mandate_limit',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='kfin_mandate_payer',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='kfin_mandate_umrn',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='nse_mandate_bank',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='nse_mandate_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='nse_mandate_limit',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='contact',
            name='nse_mandate_payer',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='nse_mandate_umrn',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
