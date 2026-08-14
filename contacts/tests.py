from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Contact, BankAccount, FamilyMember, Nominee


class ContactSearchViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.c1 = Contact.objects.create(
            name='Daniel Vogel', email='daniel@example.com'
        )
        self.c2 = Contact.objects.create(
            name='Eva Green', email='eva@cinema.org'
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

    def test_contact_list_search_no_results(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:contact_list'), {'q': 'NonExistentQuery'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 0)
        self.assertContains(response, 'No contacts found.')


class ContactImportViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_import_contacts_csv_upload(self):
        self.client.login(username='testuser', password='password123')
        csv_content = b"Name,Email\nMichael Scott,michael@dundermifflin.com\nDwight Schrute,dwight@dundermifflin.com"
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
            name='Pam Beesly',
            email='pam@dundermifflin.com',
            mobile_no='1234567890',
            pan_no='ABCDE1234F',
            state='Pennsylvania'
        )

    def test_export_contacts_csv_endpoint(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:export_contacts') + '?format=csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        content = response.content.decode('utf-8')

        # Check that headers include all model field labels
        self.assertIn('Name', content)
        self.assertIn('Email Address', content)
        self.assertIn('Mobile No', content)
        self.assertIn('PAN No', content)
        self.assertIn('State', content)
        self.assertIn('Nominee Name', content)
        self.assertIn('Father Name', content)

        # Check contact values in row
        self.assertIn('Pam Beesly', content)
        self.assertIn('pam@dundermifflin.com', content)
        self.assertIn('1234567890', content)
        self.assertIn('ABCDE1234F', content)
        self.assertIn('Pennsylvania', content)

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
        Contact.objects.create(name='Jim Halpert', email='jim@dundermifflin.com')
        response = self.client.get(reverse('contacts:export_contacts') + '?format=csv&q=Pam')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('pam@dundermifflin.com', content)
        self.assertNotIn('jim@dundermifflin.com', content)


class ContactFilterViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.c1 = Contact.objects.create(
            name='Ryan Howard', email='ryan@dundermifflin.com'
        )
        self.c2 = Contact.objects.create(
            name='Andy Bernard', email='andy@dundermifflin.com'
        )

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
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='john.doe@example.com')
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.father_name, 'Robert Doe')

    def test_add_contact_with_multiple_bank_accounts(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'mobile_no': '+1999888777',
            'name': 'Multiple Banks User',
            'dob': '1995-08-20',
            'email': 'multibank@example.com',
            'bank_accounts-TOTAL_FORMS': '2',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'bank_accounts-0-account_type': 'Savings Account',
            'bank_accounts-0-bank_name': 'HDFC Bank',
            'bank_accounts-0-account_no': '111122223333',
            'bank_accounts-0-ifsc_code': 'HDFC0001234',
            'bank_accounts-0-micr_code': '600240001',
            'bank_accounts-1-account_type': 'Current Account',
            'bank_accounts-1-bank_name': 'ICICI Bank',
            'bank_accounts-1-account_no': '444455556666',
            'bank_accounts-1-ifsc_code': 'ICIC0005678',
            'bank_accounts-1-micr_code': '600229002',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='multibank@example.com')
        self.assertEqual(contact.bank_accounts.count(), 2)
        
        savings = contact.bank_accounts.get(account_type='Savings Account')
        self.assertEqual(savings.bank_name, 'HDFC Bank')
        self.assertEqual(savings.account_no, '111122223333')

        current = contact.bank_accounts.get(account_type='Current Account')
        self.assertEqual(current.bank_name, 'ICICI Bank')
        self.assertEqual(current.account_no, '444455556666')

    def test_add_contact_with_dynamic_family_members(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'mobile_no': '+1888777666',
            'name': 'Dynamic Family User',
            'dob': '1988-12-10',
            'email': 'family@example.com',
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '3',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'family_members-0-relationship': 'Brother',
            'family_members-0-name': 'Alex Johnson',
            'family_members-0-dob': '1992-03-15',
            'family_members-0-mobile': '+1555444333',
            'family_members-1-relationship': 'Sister',
            'family_members-1-name': 'Sarah Johnson',
            'family_members-1-dob': '1996-07-22',
            'family_members-1-mobile': '+1555444334',
            'family_members-2-relationship': 'Guardian',
            'family_members-2-name': 'Uncle Bob',
            'family_members-2-mobile': '+1555444335',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='family@example.com')
        self.assertEqual(contact.family_members.count(), 3)
        self.assertTrue(contact.family_members.filter(relationship='Brother', name='Alex Johnson').exists())
        self.assertTrue(contact.family_members.filter(relationship='Sister', name='Sarah Johnson').exists())
        self.assertTrue(contact.family_members.filter(relationship='Guardian', name='Uncle Bob').exists())

    def test_add_contact_with_dynamic_nominees(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'mobile_no': '+1777666555',
            'name': 'Dynamic Nominees User',
            'dob': '1985-06-18',
            'email': 'nominees@example.com',
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '2',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'nominees-0-name': 'Primary Nominee',
            'nominees-0-relationship': 'Spouse',
            'nominees-0-dob': '1987-04-12',
            'nominees-0-mobile': '+1777666001',
            'nominees-0-email': 'nominee1@example.com',
            'nominees-1-name': 'Secondary Nominee',
            'nominees-1-relationship': 'Child',
            'nominees-1-dob': '2010-09-05',
            'nominees-1-mobile': '+1777666002',
            'nominees-1-email': 'nominee2@example.com',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='nominees@example.com')
        self.assertEqual(contact.nominees.count(), 2)
        self.assertTrue(contact.nominees.filter(name='Primary Nominee', relationship='Spouse').exists())
        self.assertTrue(contact.nominees.filter(name='Secondary Nominee', relationship='Child').exists())
        # Check synced legacy field
        self.assertEqual(contact.nominee_name, 'Primary Nominee')

    def test_add_contact_with_pan_and_aadhar_documents(self):
        self.client.login(username='testuser', password='password123')
        pan_file = SimpleUploadedFile("pan_card.pdf", b"PAN content", content_type="application/pdf")
        aadhar_file = SimpleUploadedFile("aadhar_card.pdf", b"Aadhaar content", content_type="application/pdf")
        data = {
            'mobile_no': '+1666555444',
            'name': 'Doc Upload User',
            'dob': '1991-03-25',
            'email': 'docs@example.com',
            'pan_no': 'ABCDE9999F',
            'pan_doc': pan_file,
            'aadhar_no': '9999 8888 7777',
            'aadhar_doc': aadhar_file,
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='docs@example.com')
        self.assertTrue(bool(contact.pan_doc))
        self.assertTrue(bool(contact.aadhar_doc))

    def test_add_contact_with_dynamic_mandates(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'mobile_no': '+1888999000',
            'name': 'Dynamic Mandate User',
            'dob': '1988-11-20',
            'email': 'mandateuser@example.com',
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '2',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
            'mandates-0-provider': 'BSE',
            'mandates-0-bank_name': 'HDFC Bank',
            'mandates-0-mandate_id': 'BSE123456',
            'mandates-0-mandate_limit': '100000',
            'mandates-0-payer_name': 'Dynamic Mandate User',
            'mandates-0-umrn': 'UMRN987654',
            'mandates-1-provider': 'CAMS',
            'mandates-1-bank_name': 'ICICI Bank',
            'mandates-1-mandate_id': 'CAMS654321',
            'mandates-1-mandate_limit': '50000',
            'mandates-1-payer_name': 'Dynamic Mandate User',
            'mandates-1-umrn': 'UMRN123456',
        }
        response = self.client.post(reverse('contacts:add_contact'), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        contact = Contact.objects.get(email='mandateuser@example.com')
        self.assertEqual(contact.mandates.count(), 2)
        self.assertTrue(contact.mandates.filter(provider='BSE', mandate_id='BSE123456').exists())
        self.assertTrue(contact.mandates.filter(provider='CAMS', mandate_id='CAMS654321').exists())
        # Check synced legacy field
        self.assertEqual(contact.bse_mandate_id, 'BSE123456')
        self.assertEqual(contact.cams_mandate_id, 'CAMS654321')

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


class ContactEditViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.contact = Contact.objects.create(
            name='Alice Smith',
            email='alice.smith@example.com',
            mobile_no='9876543210',
            dob='1990-01-01',
            state='New York'
        )

    def test_edit_contact_get_request(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('contacts:edit_contact', kwargs={'pk': self.contact.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Contact')
        self.assertContains(response, 'Alice Smith')
        self.assertEqual(response.context['form'].instance, self.contact)

    def test_edit_contact_post_success(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'name': 'Alice Johnson',
            'mobile_no': '9998887770',
            'dob': '1992-04-10',
            'email': 'alice.smith@example.com',
            'state': 'California',
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(reverse('contacts:edit_contact', kwargs={'pk': self.contact.pk}), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Alice Johnson')
        self.assertEqual(self.contact.mobile_no, '9998887770')
        self.assertEqual(self.contact.state, 'California')

    def test_remove_uploaded_document(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        self.client.login(username='testuser', password='password123')
        test_file = SimpleUploadedFile("pan.pdf", b"file_content", content_type="application/pdf")
        self.contact.pan_doc = test_file
        self.contact.save()

        self.assertTrue(bool(self.contact.pan_doc))

        data = {
            'name': self.contact.name,
            'mobile_no': self.contact.mobile_no,
            'dob': '1990-01-01',
            'email': self.contact.email,
            'pan_doc-clear': 'on',
            'bank_accounts-TOTAL_FORMS': '0',
            'bank_accounts-INITIAL_FORMS': '0',
            'bank_accounts-MIN_NUM_FORMS': '0',
            'bank_accounts-MAX_NUM_FORMS': '1000',
            'family_members-TOTAL_FORMS': '0',
            'family_members-INITIAL_FORMS': '0',
            'family_members-MIN_NUM_FORMS': '0',
            'family_members-MAX_NUM_FORMS': '1000',
            'nominees-TOTAL_FORMS': '0',
            'nominees-INITIAL_FORMS': '0',
            'nominees-MIN_NUM_FORMS': '0',
            'nominees-MAX_NUM_FORMS': '1000',
            'mandates-TOTAL_FORMS': '0',
            'mandates-INITIAL_FORMS': '0',
            'mandates-MIN_NUM_FORMS': '0',
            'mandates-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(reverse('contacts:edit_contact', kwargs={'pk': self.contact.pk}), data)
        self.assertRedirects(response, reverse('contacts:contact_list'))
        self.contact.refresh_from_db()
        self.assertFalse(bool(self.contact.pan_doc))

    def test_delete_contact_view(self):
        self.client.login(username='testuser', password='password123')
        contact_id = self.contact.pk
        response = self.client.post(reverse('contacts:delete_contact', kwargs={'pk': contact_id}))
        self.assertRedirects(response, reverse('contacts:contact_list'))
        self.assertFalse(Contact.objects.filter(pk=contact_id).exists())







