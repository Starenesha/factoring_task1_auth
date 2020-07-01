from django.test import TestCase, Client
# Create your tests here.
from accounts.views import send_phone_number
from django.urls import reverse

from accounts.forms import PhoneForm


class TestUserAuth(TestCase):

    def test_new_user_emloyee(self):
        '''When registered first member and model User is empty, a member should be an employee'''

        c = Client()
        request = c.get((reverse('accounts:signup_init')))
        self.assertEqual(request.status_code, 200)

        response = c.post((reverse('accounts:signup_init')), data={'phone_number': '380981111111'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, (reverse('accounts:RegistrationView_url')))

