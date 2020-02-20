# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=255, error_messages={
                           'required': 'Nimi täytyy antaa'})
    email = forms.EmailField(required=True, max_length=128, error_messages={
                             'required': 'Sähköposti täytyy antaa'})
    subject = forms.CharField(max_length=255, required=False)
    message = forms.CharField(required=True, widget=forms.Textarea, error_messages={
                              'required': 'Viesti täytyy antaa'})
    info = forms.CharField(required=False)

    def send_email(self):
        receipients = ["pelkonen.sirkka@gmail.com"]
        send_mail(
            self.cleaned_data['subject'],
            self.cleaned_data['message'],
            self.cleaned_data['email'],
            receipients
        )
