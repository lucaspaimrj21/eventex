from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        ''' GET / MUST RETURN STATUS CODE 200'''
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        ''' MUST USE INDEX.HTML'''
        self.assertTemplateUsed(self.response, 'index.html')
