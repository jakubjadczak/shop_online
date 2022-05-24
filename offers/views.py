from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import OfferForms, PhotoForms
from .models import Photo, Offer, Bought
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


class AddOffer(LoginRequiredMixin, View):

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


class AddPhotos(LoginRequiredMixin, View):

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
            messages.add_message(request, messages.SUCCESS, 'Oferta dodana')
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

        # del request.session['cat']
        # del request.session['search']

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
        paginator_result = Paginator(result, 10)
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

        paginator_result = Paginator(result, 10)
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
            result = result.filter(active=True)
        elif cat:
            result = Offer.objects.filter(categories__in=list(cat))
            result = result.filter(active=True)
        elif search:
            result = Offer.objects.filter(title__contains=search)
            result = result.filter(active=True)

        if result:
            return result
        return Offer.objects.all()


def offer_detail(request, result_id):
    offer = Offer.objects.get(pk=result_id)
    photos = Photo.objects.filter(offer_id=offer.id)
    request.session['offer_to_buy'] = offer.id

    context = {'offer': offer,
               'photos': photos,
               }
    return render(
        request=request,
        template_name='offers/offer_detail.html',
        context=context
    )


class MyOffers(LoginRequiredMixin, View):

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


@login_required
def delete_offer(request, result_id):
    offer = Offer.objects.filter(pk=result_id)
    offer.delete()
    messages.add_message(request, messages.SUCCESS, 'Usunięto oferte')
    return redirect(reverse('offer:my_offer'))


@login_required
def edit_offer(request, result_id):
    offer = get_object_or_404(Offer, pk=result_id)
    if request.method == 'POST':
        form = OfferForms(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            request.session['offer'] = result_id
            messages.add_message(request, messages.SUCCESS, 'Oferta została zedytowana')
            return redirect(reverse('offer:add_photos'))
    else:
        form = OfferForms(instance=offer)

    return render(
        request=request,
        template_name='offers/add_offer.html',
        context={'form': form}
    )


class BuyingItem(LoginRequiredMixin, View):

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        offer = Offer.objects.get(pk=request.session['offer_to_buy'])

        city = request.POST.get('city')
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        card_owner = request.POST.get('card_owner')
        card_number = request.POST.get('card_number')
        card_expiration = request.POST.get('card_expiration')

        bought = Bought(buyer=user, seller=offer.owner, offer=offer)
        bought.save()

        offer.active = False
        offer.bought_date = date.today()

        print(city)
        print(address)
        print(zip)
        print(card_owner)
        print(card_number)
        print(card_expiration)

        messages.add_message(request, messages.SUCCESS, 'Zamówienie zostało złożone')
        return redirect(reverse('main:home'))

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        offer = Offer.objects.get(pk=request.session['offer_to_buy'])

        context = {
            'user': user,
            'offer': offer,
        }
        return render(
            request=request,
            template_name='offers/buying.html',
            context=context
        )


def basket(request, offer_id):
    try:
        offer = (offer_id, )
        request.session['basket'] += offer
    except KeyError:
        offer = (offer_id,)
        request.session['basket'] = ()
        request.session['basket'] += offer

    messages.add_message(request, messages.SUCCESS, 'Dodano produkt do koszyka')
    return redirect(reverse('main:home'))


class BasketBuyPage(LoginRequiredMixin, View):

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        offers = request.session['basket']
        del request.session['basket']
        offers = [Offer.objects.get(pk=offer_id) for offer_id in offers]

        city = request.POST.get('city')
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        card_owner = request.POST.get('card_owner')
        card_number = request.POST.get('card_number')
        card_expiration = request.POST.get('card_expiration')

        for offer in offers:
            bought = Bought(buyer=user, seller=offer.owner, offer=offer)
            bought.save()


        print(city)
        print(address)
        print(zip)
        print(card_owner)
        print(card_number)
        print(card_expiration)

        messages.add_message(request, messages.SUCCESS, 'Zamówienie zostało złożone')
        return redirect(reverse('main:home'))

    @staticmethod
    def get(request, *args, **kwargs):

        print(request.session['basket'], '----')
        user = request.user
        offers = request.session['basket']
        sum = 0
        offers_list = []

        amount = len(offers)
        for offer_id in offers:
            try:
                offers_list.append(Offer.objects.get(pk=offer_id))
            except ObjectDoesNotExist:
                pass

        for offer in offers_list:
            sum += offer.price

        context = {
            'user': user,
            'offers': offers_list,
            'sum': sum,
            'amount': amount
        }
        return render(
            request=request,
            template_name='offers/basket_buy.html',
            context=context
        )


class MyBought(LoginRequiredMixin, View):

    @staticmethod
    def post(request, *args, **kwargs):

        return render(
            request=request,
            template_name='offers/my_bought.html',
        )

    @staticmethod
    def get(request, *args, **kwargs):
        array = []
        bought = Bought.objects.filter(buyer=request.user)
        for b in bought:
            array.append(b.offer)

        context = {'result_list': array}
        return render(
            request=request,
            template_name='offers/my_bought.html',
            context=context
        )