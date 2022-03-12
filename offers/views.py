from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import OfferForms, PhotoForms
from .models import Photo, Offer


class AddOffer(View):

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        form = OfferForms(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            request.session['offer'] = instance.id
            return redirect(reverse('offer:add_photos'))
        return render(
            request=request,
            template_name='offers/add_offer.html',
            context={'form': form}
        )

    @staticmethod
    def get(request, *args, **kwargs):

        form = OfferForms()
        return render(
            request=request,
            template_name='offers/add_offer.html',
            context={'form': form}
        )


class AddPhotos(View):

    @staticmethod
    def post(request, *args, **kwargs):
        idt = request.session['offer']
        offer = Offer.objects.get(pk=idt)
        PhotoFormSet = modelformset_factory(Photo, form=PhotoForms)
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.offer = offer
                    instance.save()
                    print('ok')
        return render(
            request=request,
            template_name='offers/add_photos_to_offer.html'
        )

    @staticmethod
    def get(request, *args, **kwargs):
        PhotoFormsSet = modelformset_factory(Photo, form=PhotoForms, extra=1)
        formset = PhotoFormsSet()

        return render(
            request=request,
            template_name='offers/add_photos_to_offer.html',
            context={'formset': formset}
        )