from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription

class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self): 
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):

        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    
class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Lucas Paim', cpf='01234567890',
                    email='lucaspaimrj21@gmail.com', phone='21-99999-9999')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        ''' Valid POST should redirect to /inscricao/id'''
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))
    
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())
    
class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        ''' Invalid POST should not redirect'''
        response = self.client.post('/inscricao/', {})
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)
    
    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
