from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Contact


class ContactSearchViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.c1 = Contact.objects.create(
            first_name='Daniel', last_name='Vogel', email='daniel@example.com', tag='Enterprise'
        )
        self.c2 = Contact.objects.create(
            first_name='Eva', last_name='Green', email='eva@cinema.org', tag='VIP'
        )

    def test_contact_list_authenticated_without_query(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 2)
        self.assertEqual(response.context['search_query'], '')

    def test_contact_list_search_by_name(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'), {'q': 'Daniel'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 1)
        self.assertEqual(response.context['contacts'][0], self.c1)
        self.assertEqual(response.context['search_query'], 'Daniel')

    def test_contact_list_search_by_tag(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'), {'q': 'VIP'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 1)
        self.assertEqual(response.context['contacts'][0], self.c2)

    def test_contact_list_search_no_results(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'), {'q': 'NonExistentQuery'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 0)
        self.assertContains(response, 'No contacts found.')


from django.core.files.uploadedfile import SimpleUploadedFile


class ContactImportViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_import_contacts_csv_upload(self):
        self.client.login(username='testuser', password='password123')
        csv_content = b"First Name,Last Name,Email,Tag\nMichael,Scott,michael@dundermifflin.com,Manager\nDwight,Schrute,dwight@dundermifflin.com,Sales"
        uploaded_file = SimpleUploadedFile("contacts.csv", csv_content, content_type="text/csv")

        response = self.client.post(
            reverse('contacts:import_contacts'),
            {'import_file': uploaded_file},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertTrue(Contact.objects.filter(email='michael@dundermifflin.com').exists())
        self.assertTrue(Contact.objects.filter(email='dwight@dundermifflin.com').exists())


class ContactExportViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.c1 = Contact.objects.create(
            first_name='Pam', last_name='Beesly', email='pam@dundermifflin.com', tag='Reception'
        )

    def test_export_contacts_csv_endpoint(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:export_contacts') + '?format=csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('Pam,Beesly,pam@dundermifflin.com,Reception', response.content.decode('utf-8'))

    def test_export_contacts_excel_endpoint(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:export_contacts') + '?format=excel')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_export_filtered_contacts_endpoint(self):
        self.client.login(username='testuser', password='password123')
        Contact.objects.create(first_name='Jim', last_name='Halpert', email='jim@dundermifflin.com', tag='Sales')
        response = self.client.get(reverse('contacts:export_contacts') + '?format=csv&q=Pam')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('pam@dundermifflin.com', content)
        self.assertNotIn('jim@dundermifflin.com', content)


class ContactFilterViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.c1 = Contact.objects.create(
            first_name='Ryan', last_name='Howard', email='ryan@dundermifflin.com', tag='Temp'
        )
        self.c2 = Contact.objects.create(
            first_name='Andy', last_name='Bernard', email='andy@dundermifflin.com', tag='Sales'
        )

    def test_filter_contacts_by_tag(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'), {'tag': 'Temp'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 1)
        self.assertEqual(response.context['contacts'][0], self.c1)

    def test_filter_contacts_by_date_range(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'), {'created_at_range': 'today'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 2)


class ContactAddViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_add_contact_get_request(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:add_contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CUSTOMER DETAILS')
        self.assertContains(response, 'KYC DOCUMENT DETAILS')
        self.assertContains(response, 'KYC CID DETAILS')
        self.assertContains(response, 'ADDRESS DETAILS')
        self.assertContains(response, 'BANK DETAILS')
        self.assertContains(response, 'NOMINEE DETAILS')
        self.assertContains(response, 'FAMILY DETAILS')
        self.assertContains(response, 'MANDATE DETAILS')
        self.assertContains(response, 'NSE')
        self.assertContains(response, 'BSE')
        self.assertContains(response, 'CAMS')
        self.assertContains(response, 'KFIN')

    def test_add_contact_post_success(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'mobile_no': '+1234567890',
            'name': 'John Doe',
            'dob': '1990-05-15',
            'email': 'john.doe@example.com',
            'place_of_birth': 'Chicago',
            'alternate_no': '+0987654321',
            'pan_no': 'ABCDE1234F',
            'aadhar_no': '123456789012',
            'gst_no': '22AAAAA0000A1Z5',
            'uin': 'UIN987654321',
            'ckyc_no': 'CKYC123',
            'uiic_cid': 'UIIC456',
            'tnia_cid': 'TNIA789',
            'bse_ucc': 'BSE111',
            'nse_ucc': 'NSE222',
            'lic_cid': 'LIC333',
            'pincode': '600001',
            'post_office': 'Central H.O',
            'village': 'Chennai North',
            'street_address': '101 Gandhi Road',
            'taluk': 'Egmore',
            'district': 'Chennai',
            'state': 'Tamil Nadu',
            'savings_bank_name': 'State Bank of India',
            'savings_account_no': '123456789012',
            'father_name': 'Robert Doe',
            'mother_name': 'Mary Doe',
            'spouse_name': 'Jane Doe',
            'daughter_name': 'Emily Doe',
            'son_name': 'Tommy Doe',
            'father_height_weight': '175 cm / 70 kg',
            'nse_mandate_payer': 'John Doe',
            'nse_mandate_id': 'NSE123456',
            'bse_mandate_umrn': 'UMRN987654',
            'cams_mandate_limit': '100000',
            'kfin_mandate_bank': 'HDFC Bank',
            'tag': 'VIP'
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='john.doe@example.com')
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.father_name, 'Robert Doe')
        self.assertEqual(contact.nse_mandate_payer, 'John Doe')
        self.assertEqual(contact.nse_mandate_id, 'NSE123456')
        self.assertEqual(contact.bse_mandate_umrn, 'UMRN987654')
        self.assertEqual(contact.cams_mandate_limit, '100000')
        self.assertEqual(contact.kfin_mandate_bank, 'HDFC Bank')









    def test_add_contact_missing_mandatory_fields(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'email': 'missing@example.com',
            'place_of_birth': 'Chicago',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'name', 'This field is required.')
        self.assertFormError(response.context['form'], 'mobile_no', 'This field is required.')
        self.assertFormError(response.context['form'], 'dob', 'This field is required.')





