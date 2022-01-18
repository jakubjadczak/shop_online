from django.test import TestCase
from .utils import PasswordValidator, EmailValidator


class PasswordValidatorTestCase(TestCase):

    def test_password_rule(self):
        p = PasswordValidator()
        self.assertTrue(p.check_password_rule('Skl@p21A'))
        self.assertTrue(p.check_password_rule('Q1@qwyxYz6@!2wQ'))
        self.assertFalse(p.check_password_rule('sklep'))
        self.assertFalse(p.check_password_rule(''))
        self.assertFalse(p.check_password_rule('Sklep12Wwrt55j'))

    def test_similarity(self):
        p = PasswordValidator()
        self.assertFalse(p.password_similarity('sklep', 'Sklep'))
        self.assertTrue(p.password_similarity('Sklep12@', 'Sklep12@'))


class EmailValidatorTestCase(TestCase):

    def test_email_valid(self):
        e = EmailValidator()
        self.assertTrue(e.email_valid('jakubjadczak02@gmail.com'))
        self.assertTrue(e.email_valid('jakubjadczak@onet.pl'))
        self.assertFalse(e.email_valid('jj.pl.ddewfe2'))