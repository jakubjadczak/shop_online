from django.shortcuts import render
from django.views import View


class AddOffer(View):

    @staticmethod
    def post(request, *args, **kwargs):
        return render(
            request=request,
            template_name='offers/add_offer.html'
        )

    @staticmethod
    def get(request, *args, **kwargs):
        return render(
            request=request,
            template_name='offers/add_offer.html'
        )