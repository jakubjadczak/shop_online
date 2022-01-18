from django.shortcuts import render


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        print(first_name)
        print(last_name)
        print(email)
        print(password1)
        print(password2)
        print(address)
        print(city)
        print(zip_code)

    return render(
        request=request,
        template_name='users/register.html'
    )
