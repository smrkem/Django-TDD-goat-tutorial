from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
from unittest.mock import patch
User = get_user_model()


@patch('accounts.authentication.requests.post')
class AuthenticationTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.ca')
        user.username = 'otheruser'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('the assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'the assertion', 'audience': DOMAIN}
        )

    def test_returns_none_on_response_error(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('the assertion')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'foobard'}
        user = self.backend.authenticate('the assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.ca'}
        actual_user = User.objects.create(email='a@b.ca')
        found_user = self.backend.authenticate('the assertion')
        self.assertEqual(found_user, actual_user)

    def test_creates_new_user_if_necessary_on_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.ca'}
        found_user = self.backend.authenticate('the assertion')
        created_user = User.objects.get(email='a@b.ca')
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(found_user, created_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        backend = PersonaAuthenticationBackend()
        other_user = User(email='other@user.ca')
        other_user.username = 'otheruser'
        other_user.save()
        the_user = User.objects.create(email='a@b.ca')
        found_user = backend.get_user('a@b.ca')
        self.assertEqual(found_user, the_user)

    def test_returns_none_if_no_user_with_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(
            backend.get_user('a@b.ca')
        )
