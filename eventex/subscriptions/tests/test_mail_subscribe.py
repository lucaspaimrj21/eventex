from django.test import TestCase
from django.core import mail


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Lucas Paim', cpf='01234567890',
                    email='lucaspaimrj21@gmail.com', phone='21-99999-9999')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
    
    def test_subscription_email_subject(self):
       
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        
        expect = 'lucaspaimrj21@gmail.com'

        self.assertEqual(expect, self.email.from_email)    

    def test_subscription_email_to(self):
        
        expect = ['lucaspaimrj21@gmail.com', 'lucaspaimrj21@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Lucas Paim',
                     '01234567890',
                     'lucaspaimrj21@gmail.com',
                     '21-99999-9999',]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

