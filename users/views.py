from django.shortcuts import render, redirect
from .utils import PasswordValidator, EmailValidator, random_code_for_reset_password
from .models import CustomUser
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import account_activate_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from threading import Thread


class EmailSendThread(Thread):
    """
    Redirect to login page without waiting for send email
    """
    def __init__(self, email):
        Thread.__init__(self)
        self.email = email

    def run(self):
        self.email.send()


class RegisterPage(View):

    @staticmethod
    def post(request, *args, **kwargs):
        p = PasswordValidator()
        e = EmailValidator()
        has_error = False
        context = {'data': request.POST}
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        if not first_name and last_name and email:
            has_error = True
            messages.error(request, 'Musisz uzupełnić wszystkie pola')

        if not p.check_password_rule(str(password1)):
            has_error = True
            messages.error(request, 'Hasło musi mieć jedną wielką litere, jedną małą, cyfre, znak i min 7 znaków')

        if not p.password_similarity(str(password1), str(password2)):
            has_error = True
            messages.error(request, 'Hasła się różnią')

        if not e.email_valid(str(email)):
            has_error = True
            messages.error(request, 'Wprowadź prawidłowy email')

        if not e.email_unique(str(email)):
            has_error = True
            messages.error(request, 'Konto z takim emailem już istnieje')

        if not has_error:
            user = CustomUser.objects.create_user(username=email, email=email, first_name=first_name,
                                                  last_name=last_name, address=address, city=city, zip_code=zip_code)
            user.set_password(password1)
            user.is_active = False
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Konto zostało pomyślnie założone,'
                                                            ' zobacz swojego maila w celu aktywacji')
            # Sending activation email

            # self.send_email(user, get_current_site(request))

            return render(
                request=request,
                template_name='users/login.html',
                context=context,
            )

        return render(
            request=request,
            template_name='users/register.html',
            context=context,
        )

    @staticmethod
    def get(request, *args, **kwargs):
        return render(
            request=request,
            template_name='users/register.html'
        )

    @staticmethod
    def send_email(user, current_site):

        current_site = current_site
        mail_subject = 'Aktywuj swoje konto'
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activate_token.make_token(user)
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        EmailSendThread(email).start()


def activate(request, uidb64, token):
    """
    Activate account from send email
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Email został zweryfikowany')
        return redirect(reverse('logowanie'))
    else:
        messages.add_message(request, messages.ERROR, 'Nie udało się zweryfikować maila,'
                                                      ' kliknij zaloguj się by spróbować ponownie')
        return redirect(reverse('register:acc_info'))


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user_check = False

        user = authenticate(request, username=username, password=password)
        if CustomUser.objects.filter(username=username).exists():
            user_check = CustomUser.objects.get(username=username)

        if not user and not user_check:
            messages.error(request, 'Złe dane')

        elif user and user_check:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Zalogowano!')
            return redirect(reverse('main:home'))

        elif not user and not user_check.is_active:
            messages.add_message(request, messages.ERROR, 'Zobacz swojego maila!')
            return redirect(reverse('users:login'))

    return render(
        request=request,
        template_name='users/login.html'
    )


def user_logout(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS, 'Wylogowano!')
    return redirect(reverse('users:login'))


@login_required
def my_account_page(request):
    return render(
        request=request,
        template_name='users/my_account.html'
    )


@login_required
def change_password(request):
    if request.method == 'POST':
        p = PasswordValidator()
        has_error = False
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        user = request.user
        if user.check_password(old_password):
            if not p.check_password_rule(str(password1)):
                has_error = True
                messages.error(request, 'Hasło musi mieć jedną wielką litere, jedną małą, cyfre, znak i min 7 znaków')

            if not p.password_similarity(str(password1), str(password2)):
                has_error = True
                messages.error(request, 'Hasła się różnią')

            if not has_error:
                user.set_password(password1)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Hasło zostało zmienione!')

        elif old_password is not None:
            messages.add_message(request, messages.ERROR, 'Wprowadź dobre hasło!')
        return render(
            request=request,
            template_name='users/change_password.html'
        )
    else:
        return render(
            request=request,
            template_name='users/change_password.html'
        )


class ResetPasswordSendCode(View):
    e = EmailValidator()

    def post(self, request, *args, **kwargs):
        has_error = False
        email = request.POST.get('email')
        if not self.e.email_valid(str(email)):
            has_error = True
            messages.error(request, 'Email nie poprawny')

        if not CustomUser.objects.filter(email=email).exists():
            has_error = True
            messages.error(request, 'Do takiego maila nie jest przpisane żadne konto')

        if not has_error:
            request.session['user_email'] = email
            code = random_code_for_reset_password()
            print(code)
            user = CustomUser.objects.get(username=email)
            user.reset_code = code
            user.save()
            # Sending activation email
            '''
            current_site = get_current_site(request)
            mail_subject = 'Zmień hasło'
            message = render_to_string('users/activation_email.html', {
                'code': code
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
'''
            # end

        return render(
            request=request,
            template_name='users/reset_password.html'
        )

    @staticmethod
    def get(request, *args, **kwargs):
        return render(
            request=request,
            template_name='users/password_reset_send_code.html'
        )


class ResetPassword(View):

    @staticmethod
    def post(request, *args, **kwargs):
        p = PasswordValidator()

        has_error = False

        code = request.POST.get('reset_code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        u_email = request.session['user_email']
        user = CustomUser.objects.get(username=u_email)

        if str(u_email) != str(user.email):
            has_error = True
            messages.error(request, 'Ups, spróbuj ponownie')

        if user.reset_code != code:
            has_error = True
            messages.error(request, 'Kod się nie zgadza')

        if not p.check_password_rule(str(password1)):
            has_error = True
            messages.error(request, 'Hasło musi mieć jedną wielką litere, jedną małą, cyfre, znak i min 7 znaków')

        if not p.password_similarity(str(password1), str(password2)):
            has_error = True
            messages.error(request, 'Hasła się różnią')

        if not has_error:
            user.set_password(password1)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Hasło zostało zmienione!')
            return render(
                request=request,
                template_name='users/login.html'
            )
        del request.session['user_email']
        return render(
            request=request,
            template_name='users/reset_password.html'
        )

    @staticmethod
    def get(request, *args, **kwargs):
        return render(
            request=request,
            template_name='users/reset_password.html'
        )


@login_required
def delete_account(request):
    if CustomUser.objects.filter(username=request.user.username).exists():
        user = CustomUser.objects.get(username=request.user.username)
        logout(request)
        user.delete()
        messages.add_message(request, messages.SUCCESS, 'Konto usunięte')
        return render(
            request=request,
            template_name='users/register.html'
        )
    else:
        messages.add_message(request, messages.ERROR, 'Coś poszło nie tak')
        return render(
            request=request,
            template_name='users/register.html'
        )