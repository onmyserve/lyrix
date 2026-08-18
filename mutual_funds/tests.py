from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from contacts.models import Contact
from .models import MutualFund

User = get_user_model()


class MutualFundTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        self.client.login(username='testuser', password='password123')

        self.c1 = Contact.objects.create(name='John Doe', mobile_no='9876543210', email='john@example.com', pan_no='ABCDE1234F')
        self.c2 = Contact.objects.create(name='Jane Smith', mobile_no='9123456789', email='jane@example.com', pan_no='XYZPK9876M')

        self.mf1 = MutualFund.objects.create(
            contact=self.c1, name='John Doe', mobile_no='9876543210', pan='ABCDE1234F',
            amc='HDFC Mutual Fund', sip_amt='5000', sip_date='10th', mode='Monthly',
            bank='HDFC Bank', mandate_id='MND123', folio_number='101010/11', fund_description='HDFC Top 100'
        )
        self.mf2 = MutualFund.objects.create(
            contact=self.c2, name='Jane Smith', mobile_no='9123456789', pan='XYZPK9876M',
            amc='SBI Mutual Fund', sip_amt='10000', sip_date='15th', mode='E-Mandate',
            bank='SBI Bank', mandate_id='MND999', folio_number='202020/22', fund_description='SBI Bluechip'
        )

    def test_fund_list_view_authenticated(self):
        response = self.client.get(reverse('mutual_funds:fund_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Smith')
        self.assertContains(response, 'HDFC Mutual Fund')
        self.assertContains(response, 'SBI Mutual Fund')

    def test_search_mutual_funds(self):
        response = self.client.get(reverse('mutual_funds:fund_list') + '?q=HDFC')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Smith')

    def test_add_mutual_fund_for_contact(self):
        c3 = Contact.objects.create(name='Robert Brown', mobile_no='9988776655', email='robert@example.com', pan_no='BBBCC3333K')
        url = reverse('mutual_funds:add_fund')
        response = self.client.post(url, {
            'contact': c3.pk,
            'name': 'Robert Brown',
            'mobile_no': '9988776655',
            'pan': 'BBBCC3333K',
            'amc': 'Axis Mutual Fund',
            'sip_amt': '2500',
            'sip_date': '5th',
            'mode': 'Monthly',
            'bank': 'ICICI Bank',
            'mandate_id': 'AXM12345',
            'folio_number': '303030/33',
            'fund_description': 'Axis Small Cap Fund'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MutualFund.objects.filter(contact=c3, amc='Axis Mutual Fund').exists())

    def test_add_multiple_funds_for_same_contact(self):
        url = reverse('mutual_funds:add_fund')
        self.client.post(url, {'contact': self.c1.pk, 'name': 'John Doe', 'mobile_no': '9876543210', 'amc': 'ICICI MF', 'sip_amt': '3000'})
        self.client.post(url, {'contact': self.c1.pk, 'name': 'John Doe', 'mobile_no': '9876543210', 'amc': 'Nippon India', 'sip_amt': '4000'})

        self.assertEqual(MutualFund.objects.filter(contact=self.c1).count(), 3)

    def test_edit_mutual_fund(self):
        url = reverse('mutual_funds:edit_fund', kwargs={'pk': self.mf1.pk})
        response = self.client.post(url, {
            'contact': self.c1.pk,
            'name': 'John Doe Updated',
            'mobile_no': '9876543210',
            'pan': 'ABCDE1234F',
            'amc': 'HDFC Mutual Fund Updated',
            'sip_amt': '7500'
        })
        self.assertEqual(response.status_code, 302)
        self.mf1.refresh_from_db()
        self.assertEqual(self.mf1.name, 'John Doe Updated')
        self.assertEqual(self.mf1.sip_amt, '7500')

    def test_export_csv(self):
        url = reverse('mutual_funds:export_funds') + '?format=csv'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        content = response.content.decode('utf-8')
        self.assertIn('John Doe', content)
        self.assertIn('HDFC Mutual Fund', content)

    def test_import_csv_matching_contacts_multiple_entries(self):
        c_alice = Contact.objects.create(name='Alice Cooper', mobile_no='9112233445', email='alice@example.com')

        csv_data = "name,mobile_no,amc,sip_amt,folio_number\nAlice Cooper,9112233445,UTI MF,2000,998877/11\nAlice Cooper,9112233445,DSP MF,3500,998877/22\nNonExistent Member,9999999999,Kotak MF,1000,112233\n"
        upload_file = SimpleUploadedFile("test_import.csv", csv_data.encode('utf-8'), content_type="text/csv")

        url = reverse('mutual_funds:import_funds')
        response = self.client.post(url, {'import_file': upload_file})
        self.assertEqual(response.status_code, 302)

        self.assertEqual(MutualFund.objects.filter(contact=c_alice).count(), 2)
        self.assertFalse(MutualFund.objects.filter(name='NonExistent Member').exists())

    def test_delete_mutual_fund_view(self):
        url = reverse('mutual_funds:delete_fund', kwargs={'pk': self.mf1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MutualFund.objects.filter(pk=self.mf1.pk).exists())

