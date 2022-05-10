from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from .models import Offer, Photo, Category


class AddCategory(forms.MultipleChoiceField):

    @staticmethod
    def label_from_instance(category):
        return '%s' % category.name


class OfferForms(forms.ModelForm):

    # TODO formularz dodawania
    # przy ustawianiu pol osobno {{form.title|as_crispy_field}}... nie działa tiny mce
    # szkielet rozwiązania html na końcu tego pliku
    class Meta:
        model = Offer
        fields = ['title', 'short_description', 'description', 'price', 'negotiations',
                  'titular_photo', 'categories', 'producer', 'color', 'weight', 'condition'
                 ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Dodaj ofertę',
                'title',
                'short_description',
                'description',
                'price',
                'negotiations',
                'titular_photo',
                'categories',
                'producer',
                'color',
                'weight',
                'condition',
            ),
            ButtonHolder(
                Submit('submit', 'Dalej', css_class='btn btn-primary'),
                css_class='d-flex justify-content-end'
            )
        )


class PhotoForms(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['photo']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj zdjęcia',
                    'photo'

                ),
                ButtonHolder(
                    Submit('submit', 'Dalej', css_class='btn btn-primary'),
                    css_class='d-flex justify-content-end'
                )
            )
