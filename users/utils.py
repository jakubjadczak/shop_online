from validate_email import validate_email
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from random import randint

big_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
small_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
signs = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', ':', ';', '<', '=', '>', '?', '@']
digit = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


class PasswordValidator:

    @staticmethod
    def check_password_rule(password: str) -> bool:
        """
        Password validators, capital, small letter, sign, digit
        :param password: user's password
        :return: True or False
        """
        big_letter_bool = False
        small_letter_bool = False
        signs_bool = False
        digit_bool = False
        if len(password) > 6:
            for i in range(len(big_letter)):
                if big_letter[i] in password:
                    big_letter_bool = True
                if small_letter[i] in password:
                    small_letter_bool = True

            for j in range(len(signs)):
                if signs[j] in password:
                    signs_bool = True

            for k in range(len(digit)):
                if digit[k] in password:
                    digit_bool = True

        if big_letter_bool and small_letter_bool and digit_bool and signs_bool:
            return True
        return False

    @staticmethod
    def password_similarity(password1: str, password2: str) -> bool:
        """
        Check password1 == password2
        :param password1: password
        :param password2: again password
        :return: True or False
        """
        if password1 == password2:
            return True
        return False


class EmailValidator:

    @staticmethod
    def email_valid(email: str) -> bool:
        if validate_email(email):
            return True
        return False

    @staticmethod
    def email_unique(email: str) -> bool:
        if not CustomUser.objects.filter(email=email).exists():
            return True


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activate_token = TokenGenerator()
