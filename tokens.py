from django.contrib.auth.tokens import PasswordResetTokenGenerator as Generator
from django.utils import six

class TokenGenerator(Generator):
	def _make_hash_value(self, user, timestamp):
		return(
			six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
			)

account_activation_token = TokenGenerator()
