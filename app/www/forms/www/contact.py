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
    
    def check_for_spam(self):
        info = self.cleaned_data['info']
        if info != '':
            raise ValueError('Spam detected.')    

    def get_form_errors(self):
        errors = {}
        if self.errors is None:
            return errors

        for field in self:
            for error in field.errors:
                if field not in errors:
                    errors[field.name] = str(error)
                else:
                    errors[field.name] = "%s<br>%s" % (
                        str(errors[field]), error)
        return errors

    def get_form_values(self):
        vals = {}
        if self.errors:
            for field in self:
                vals[field.name] = str(field.value())
        return vals