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



