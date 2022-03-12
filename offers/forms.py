from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from tinymce.widgets import TinyMCE

from .models import Offer, Photo


class OfferForms(forms.ModelForm):

    # TODO wygląd formularza dodoawania oferty to jakiś żart,
    # przy ustawianiu pol osobno {{form.title|as_crispy_field}}... nie działa tiny mce
    # szkielet rozwiązania html na końcu tego pliku
    class Meta:
        model = Offer
        fields = ['title', 'short_description', 'description', 'price', 'negotiations',
                  'titular_photo', 'categories', 'producer', 'color', 'weight', 'condition'
                 ]
        # label

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



'''
{% block content %}
  <form method="post">
    {% csrf_token %}
    <div class="form-row">
      <div class="form-group col-md-6 mb-0">
        {{ form.title|as_crispy_field }}
      </div>
      <div class="form-group col-md-6 mb-0">
        {{ form.short_description|as_crispy_field }}
      </div>
    </div>
    {{ form.description|as_crispy_field }}
    {{ form.price|as_crispy_field }}
    <div class="form-row">
      <div class="form-group col-md-6 mb-0">
        {{ form.city|as_crispy_field }}
      </div>
      <div class="form-group col-md-4 mb-0">
        {{ form.state|as_crispy_field }}
      </div>
      <div class="form-group col-md-2 mb-0">
        {{ form.zip_code|as_crispy_field }}
      </div>
    </div>
    {{ form.check_me_out|as_crispy_field }}
    <button type="submit" class="btn btn-primary">Sign in</button>
  </form>
{% endblock %}
'''