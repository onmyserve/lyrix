from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0016_mandate'),
    ]

    operations = [
        migrations.CreateModel(
            name='MutualFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('mobile_no', models.CharField(blank=True, default='', max_length=20)),
                ('pan', models.CharField(blank=True, default='', max_length=20)),
                ('sip_amt', models.CharField(blank=True, default='', max_length=50)),
                ('sip_date', models.CharField(blank=True, default='', max_length=50)),
                ('mode', models.CharField(blank=True, default='', max_length=50)),
                ('sip_start_date', models.DateField(blank=True, null=True)),
                ('sip_end_date', models.DateField(blank=True, null=True)),
                ('bank', models.CharField(blank=True, default='', max_length=100)),
                ('mandate_id', models.CharField(blank=True, default='', max_length=50)),
                ('amc', models.CharField(blank=True, default='', max_length=100)),
                ('fund_description', models.TextField(blank=True, default='')),
                ('folio_number', models.CharField(blank=True, default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mutual_funds', to='contacts.contact')),
            ],
        ),
    ]
