from django.forms import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact

class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Lucas Paim',
            slug='lucas-paim',
            photo='https://www.timeforkids.com/wp-content/uploads/2020/08/Grace_003.jpg'
        )
    def test_email(self):
        contact = Contact.objects.create(speaker = self.speaker, kind='Contact.EMAIL',
                                         value='lucaspaimrj21@gmail.com'
        )

        self.assertTrue(Contact.objects.exists())
    
    def test_phone(self):
        contact = Contact.objects.create(speaker = self.speaker, kind='Contact.PHONE',
                                         value='21-99999-9999'
    )
        
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker = self.speaker, kind='Contact.EMAIL',
                                         value='lucaspaimrj21@gmail.com'
        )
        self.assertEqual('lucaspaimrj21@gmail.com', str(contact))

class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Lucas Paim',
            slug='lucas-paim',
            photo='http://lucaspaim.com.br'
        )
    
        s.contact_set.create(kind=Contact.EMAIL, value='lucaspaimrj21@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='21-99999-9999')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['lucaspaimrj21@gmail.com']
        self.assertQuerySetEqual(qs, expected, lambda o: o.value)
    
    def test_phone(self):
        qs = Contact.objects.phones()
        expected = ['21-99999-9999']
        self.assertQuerySetEqual(qs, expected, lambda o: o.value)