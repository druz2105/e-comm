from django import forms
from django.contrib.auth.models import User

PAYMENT_CHOICES = (('C', "COD"), ('P', "PayPal"))
COUNTRY_CHOICES = (('I', "INDIA"), ('P', "PAKISTAN"), ('B', 'Bangladesh'))


class CheckoutForm(forms.Form):
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "add1",
        "placeholder": "Apartment Number"
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "add2",
        'placeholder': "City/Village/Area"

    }))
    country = forms.CharField(widget=forms.Select(choices=COUNTRY_CHOICES, attrs={"class": "form-control"}))
    state = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "city",
        'placeholder': "state"
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "zip",
        'placeholder': "Postcode/ZIP"
    }))
    same_shipping = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    use_default_billing = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class EditProfileForm(forms.Form):
    mobile_no = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': "Mobile No", 'class': "form-control"}))
    alternate_mobile_number = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': "Alternate Mobile No", 'class': "form-control"}))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "add1",
        "placeholder": "Apartment Number"
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "add2",
        'placeholder': "City/Village/Area"

    }))
    country = forms.CharField(widget=forms.Select(choices=COUNTRY_CHOICES, attrs={"class": "form-control"}))
    state = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "city",
        'placeholder': "state"
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'id': "zip",
        'placeholder': "Postcode/ZIP"
    }))
