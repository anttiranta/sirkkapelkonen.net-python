# -*- coding: utf-8 -*-
from django.shortcuts import render
from www.forms.www.contact import ContactForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect


class ContactView(FormView):
    template_name = 'www/contact.html'
    form_class = ContactForm
    success_url = '/yhteys/'

    # Messages
    spam_message = '<h2>Viestin lähettäminen epäonnistui</h2> Tämä sähköpostiosoite on suojattu roskapostia vastaan. Jos näet tämän viestin, kyseessä on tekninen häiriö ja viestin lähettäminen ei tällä hetkellä onnistu. <br /><br /> Pahoittelemmme häiriötä. Yritä myöhemmin uudelleen.<br /><br /> <a href="/" title="Etusivu" class="underline">Palaa sivustolle&#62;&#62;&#62;</a>'
    error_message = '<h2>Viestin lähettäminen epäonnistui</h2> Viestin lähettämisessä tapahtui virhe. <br /><br /> Voit myös lähettää sähköpostia Sirkka Pelkoselle osoitteeseen <a href="mailto:pelkonen.sirkka(at)gmail.com" class="underline">pelkonen.sirkka(at)gmail.com</a>.<br /><br /><a href="/" title="Etusivu" class="underline">Palaa sivustolle&#62;&#62;&#62;</a>'
    success_message = '<h2>Kiitos viestistäsi</h2> Kiitos viestistäsi!<br /><br /> <a href="/" title="Etusivu" class="underline">Palaa sivustolle&#62;&#62;&#62;</a>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_title'] = "Sirkka Pelkonen - Yhteystiedot"
        context['active_tab'] = "contact"

        if 'message' in self.request.session:
            context['message'] = self.request.session.get('message')
            del self.request.session['message']

        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['errors'] = form.get_form_errors()
        context['values'] = form.get_form_values()

        return self.render_to_response(context)

    def form_valid(self, form):
        message = None

        try:
            form.check_for_spam()
            form.send_email()
        except ValueError as ve:
            message = self.__get_message(ve)
        except Exception as e:
            message = self.__get_message(e)

        if message == None:
            message = self.__get_message()
        return self.__go_back(message)

    def __go_back(self, message):
        self.request.session['message'] = message
        return HttpResponseRedirect(self.get_success_url())

    def __get_message(self, exception=None):
        if (exception == None):
            return self.success_message
        if (isinstance(exception, ValueError)):
            return self.spam_message
        elif (isinstance(exception, Exception)):
            return self.error_message
        return None