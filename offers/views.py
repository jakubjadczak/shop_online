from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import OfferForms, PhotoForms
from .models import Photo, Offer
from django.core.paginator import Paginator
from django.contrib import messages


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
            del request.session['offer']
            return redirect(reverse('main:home'))
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


class DisplayOffer(View):

    def post(self, request, *args, **kwargs):

        del request.session['cat']
        del request.session['search']

        # 2 lines above are responsible for clear a cache search memory after click "Usun filtry" button
        # to get against all results

        cat = request.POST.getlist('cat')
        search = request.POST.get('search')
        cat = [int(i) for i in cat]

        request.session['cat'] = cat
        request.session['search'] = search

        result = self.get_result(cat, search)

        # result = set(result)  # against duplicates
        # result = list(result)
        paginator_result = Paginator(result, 2)
        p = paginator_result.page(2)
        print(p.has_previous())
        page_number = request.GET.get('page')
        page_obj = paginator_result.get_page(page_number)

        context = {
            'result_list': page_obj,
        }

        return render(
            request=request,
            template_name='main/home.html',
            context=context,
        )

    def get(self, request, *args, **kwargs):
        if request.session['cat'] or request.session['search']:
            cat = request.session['cat']
            search = request.session['search']
            result = self.get_result(cat, search)
        else:
            result = Offer.objects.all().order_by('id')

        paginator_result = Paginator(result, 2)
        p = paginator_result.page(2)
        print(p.has_previous())
        page_number = request.GET.get('page')
        page_obj = paginator_result.get_page(page_number)

        context = {
            'result_list': page_obj,
        }
        return render(
            request=request,
            template_name='main/home.html',
            context=context,
        )

    @staticmethod
    def get_result(cat, search):
        result = []
        if cat and search:
            result = Offer.objects.filter(categories__in=list(cat))
            result = result.filter(title__icontains=search)
        elif cat:
            result = Offer.objects.filter(categories__in=list(cat))
        elif search:
            result = Offer.objects.filter(title__contains=search)

        if result:
            return result
        return Offer.objects.all()


def offer_detail(request, result_id):
    offer = Offer.objects.get(pk=result_id)
    photos = Photo.objects.filter(offer_id=offer.id)

    context = {'offer': offer,
               'photos': photos,
               }
    return render(
        request=request,
        template_name='offers/offer_detail.html',
        context=context
    )


class MyOffers(View):

    @staticmethod
    def post(request, *args, **kwargs):

        return render(
            request=request,
            template_name='offers/my_offers.html'
        )

    @staticmethod
    def get(request, *args, **kwargs):
        result = Offer.objects.filter(owner_id=request.user)

        paginator_result = Paginator(result, 2)
        page_number = request.GET.get('page')
        page_obj = paginator_result.get_page(page_number)

        context = {
            'result_list': page_obj,
        }

        return render(
            request=request,
            template_name='offers/my_offers.html',
            context=context
        )


def delete_offer(request, result_id):
    offer = Offer.objects.filter(pk=result_id)
    offer.delete()
    messages.add_message(request, messages.SUCCESS, 'Usunięto oferte')
    return redirect(reverse('offer:my_offer'))


def edit_offer(request, result_id):
    offer = get_object_or_404(Offer, pk=result_id)
    if request.method == 'POST':
        form = OfferForms(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            request.session['offer'] = result_id
            return redirect(reverse('offer:add_photos'))
    else:
        form = OfferForms(instance=offer)

    return render(
        request=request,
        template_name='offers/add_offer.html',
        context={'form': form}
    )

