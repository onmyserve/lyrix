from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BankDetail


class BankDetailModelTest(TestCase):
    def test_create_bank_detail(self):
        bank = BankDetail.objects.create(
            bank_name="State Bank of India",
            ifsc_code="SBIN0001234",
            micr_code="400002001",
            branch_name="Main Branch"
        )
        self.assertEqual(str(bank), "State Bank of India (SBIN0001234)")
        self.assertEqual(BankDetail.objects.count(), 1)


class BankDetailViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.bank = BankDetail.objects.create(
            bank_name="HDFC Bank",
            ifsc_code="HDFC0001111",
            micr_code="400240002",
            branch_name="Bandra Branch"
        )

    def test_bank_detail_list_view(self):
        response = self.client.get(reverse('bank_details:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HDFC Bank")
        self.assertContains(response, "HDFC0001111")

    def test_add_bank_detail_view(self):
        response = self.client.post(reverse('bank_details:add'), {
            'bank_name': 'ICICI Bank',
            'ifsc_code': 'ICIC0002222',
            'micr_code': '400229001',
            'branch_name': 'Andheri'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BankDetail.objects.filter(ifsc_code='ICIC0002222').exists())

    def test_edit_bank_detail_view(self):
        response = self.client.post(reverse('bank_details:edit', args=[self.bank.pk]), {
            'bank_name': 'HDFC Bank Limited',
            'ifsc_code': 'HDFC0001111',
            'micr_code': '400240002',
            'branch_name': 'Bandra West'
        })
        self.assertEqual(response.status_code, 302)
        self.bank.refresh_from_db()
        self.assertEqual(self.bank.bank_name, 'HDFC Bank Limited')

    def test_delete_bank_detail_view(self):
        response = self.client.post(reverse('bank_details:delete', args=[self.bank.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BankDetail.objects.filter(pk=self.bank.pk).exists())

    def test_search_bank_detail(self):
        response = self.client.get(reverse('bank_details:list') + '?q=HDFC0001111')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HDFC0001111")

        response = self.client.get(reverse('bank_details:list') + '?q=NONEXISTENT')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "HDFC0001111")

    def test_bank_detail_lookup_api(self):
        response = self.client.get(reverse('bank_details:api_lookup') + '?ifsc=HDFC0001111')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('found'))
        self.assertEqual(data.get('bank_name'), 'HDFC Bank')
        self.assertEqual(data.get('micr_code'), '400240002')

        response = self.client.get(reverse('bank_details:api_lookup') + '?ifsc=INVALID99999')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get('found'))
