from django.shortcuts import render, redirect
from .utils import PasswordValidator, EmailValidator
from .models import CustomUser
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import account_activate_token

def register_page(request):
    p = PasswordValidator()
    e = EmailValidator()
    has_error = False
    if request.method == 'POST':
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
            messages.success(request, 'Konto zostało pomyślnie założone, zobacz swojego maila w celu aktywacji')
            # Sending activation email

            current_site = get_current_site(request)
            mail_subject = 'Aktywuj konto na melinie'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activate_token.make_token(user)
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            # end

        else:
            return render(
                request=request,
                template_name='users/register.html',
                context=context,
            )
    return render(
        request=request,
        template_name='users/register.html'
    )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activate_token.check_token(user, token):
        user.is_active = True
        user.save()
        redirect(reverse('logowanie'))
        messages.info(request, 'Email został zweryfikowany')
        return render(
            request=request,
            template_name='logowanie',
        )
    else:
        redirect(reverse('register:acc_info'))
        messages.info(request, 'Link aktywacyjny wygasł')
        return render(
            request=request,
            template_name='nie zweryfikowany',
            context={'first': 'Coś poszło nie tak', 'second': 'Kliknij tu by dostać kolejnego maila'}
        )
