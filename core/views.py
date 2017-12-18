from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from .models import Fragment, Document, Quote, QuoteAccessLogEntry
from .models import Fragment, Document, Quote
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import random
from datetime import datetime


def index(request):
    #return HttpResponse("Nine Worlds Deep")

    # adapting from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page

    # counts 
    num_frags = Fragment.objects.all().count()
    num_docs = Document.objects.all().count()
    num_quotes = Quote.objects.all().count()
    num_users = User.objects.all().count()

    # number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
 
    # populate with these quotes if none exist
    if num_quotes < 1:
        #for testing
        q = Quote(text="\"The most merciful thing in the world, I think, is the inability of the human mind to correlate all its contents. We live on a placid island of ignorance in the midst of black seas of infinity, and it was not meant that we should voyage far. The sciences, each straining in its own direction, have hitherto harmed us little; but some day the piecing together of dissociated knowledge will open up such terrifying vistas of reality, and of our frightful position therein, that we shall either go mad from the revelation or flee from the light into the peace and safety of a new dark age.\" -- H.P. Lovecraft", public_accessible=True)
        q.save()
        q = Quote(text="\"Inevitably anyone with an independent mind must become 'one who resists or opposes authority or established conventions': a rebel. If enough people come to agree with, and follow, the Rebel, we now have a Devil. Until, of course, still more people agree. And then, finally, we have --- Greatness.\" -- Aleister Crowley", public_accessible=True)
        q.save()
        q = Quote(text="\"Atavistic resurgence, a primal urge towards union with the Divine by returning to the common source of all, is indicated by the backward symbolism peculiar to all Sabbath ceremonies, as also of many ideas connected with witchcraft, sorcery and magic. Whether it be the symbol of the moon presiding over nocturnal ecstasies; the words of power chanted backwards; the back-to-back dance performed in opposition to the sun's course; the devil's tail - are all instances of reversal and symbolic of Will and Desire turning within and down to subconscious regions, to the remote past, there to surprise the required atavistic energy for purposes of transformation, healing, initiation, construction or destruction.\" -- Kenneth Grant, Hidden Lore: Hermetic Glyphs", public_accessible=True)
        q.save()
    
    #these numbers are for testing, increase when working
    num_quotes_to_retrieve = 5
    num_quotes_to_randomize = 3

    if request.user.is_authenticated:

        # grab X quotes, select where public_accessible is true or owner is logged in user
        quote_queryset = Quote.objects.filter(Q(owner=request.user)|Q(public_accessible=True)).order_by("last_accessed")[:num_quotes_to_retrieve]
        pass

    else:

        # grab X publicly accessible quotes, select from most recent by id
        quote_queryset = Quote.objects.filter(public_accessible=True).order_by("last_accessed")[:num_quotes_to_retrieve]

    #take retrieved quotes and randomize to grab Y quotes and add to variable random_quotes
    quote_list = random.sample(list(quote_queryset), num_quotes_to_randomize)


    for quote in quote_list:
        quote.last_accessed = datetime.now()
        quote.save()


    # render
    return render(
        request,
        'index.html',
        context = {
            'num_frags':num_frags, 
            'num_docs':num_docs, 
            'num_quotes':num_quotes,
            'num_visits': num_visits,
            'num_users':num_users,
            'quote_list': quote_list,
        },
    )


class DocumentListView(generic.ListView):
    model = Document
    paginate_by = 2 #low for testing, increase for production

class DocumentDetailView(generic.DetailView):
    model = Document

class QuoteListView(generic.ListView):
    model = Quote

class QuoteDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Quote

    def test_func(self):
        """ Only let the user access this page if they own the quote being updated"""
        return self.get_object().public_accessible or self.get_object().owner == self.request.user 

class QuotesPrivateForUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class based view listing quotes added by users
    """
    model = Quote
    template_name = 'core/quote_list_private_for_user.html'
    paginate_by = 5

    def get_queryset(self):
        return Quote.objects.filter(Q(owner=self.request.user)|Q(public_accessible=True)).order_by('-created_at')


class QuoteCreate(CreateView):
    model = Quote
    fields = ['text', 'public_accessible',]

    def form_valid(self, form):
        quote = form.save(commit=False)
        quote.owner = self.request.user
        quote.save()
        # return HttpResponseRedirect(reverse("quote-detail", args=(quote.id,)))
        return HttpResponseRedirect(reverse("my-quotes"))

class QuoteUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quote
    fields = ['text', 'public_accessible',]

    def test_func(self):
        """ Only let the user access this page if they own the quote being updated"""
        return self.get_object().owner == self.request.user

class QuoteDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy('quotes')        

    def test_func(self):
        """ Only let the user access this page if they own the object being deleted"""
        return self.get_object().owner == self.request.user