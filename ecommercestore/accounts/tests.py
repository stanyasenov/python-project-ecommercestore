from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ecommercestore.accounts.models import Customer

UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qew',
    }
    VALID_PROFILE_DATA = {
        'name': 'Test',
        'email': 'test@mail.bg',
    }

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        customer = Customer.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return user, customer

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': 1,}))
        self.assertEqual(404, response.status_code)

    def test_when_all_valid_expect_correct_template(self):
        user, customer = self.__create_valid_user_and_profile()

        self.client.get(reverse('profile details', kwargs={'pk': 2}))

        self.assertTemplateUsed('store/profile.html')


class UserRegistrationView(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qew',
    }
    VALID_PROFILE_DATA = {
        'name': 'Test',
        'email': 'test@mail.bg',
    }

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        customer = Customer.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return user, customer

    def test_when_all_valid_expect_correct_template(self):
        user, customer = self.__create_valid_user_and_profile()

        self.client.get(reverse('profile details', kwargs={'pk': 2}))

        self.assertTemplateUsed('store/profile.html')