from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Fragment, Document, Quote
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin


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
        return Quote.objects.filter(owner=self.request.user).filter(public_accessible=False).order_by('created_at')


class QuoteCreate(CreateView):
    model = Quote
    fields = ['text', 'public_accessible',]

    def form_valid(self, form):
        quote = form.save(commit=False)
        quote.owner = self.request.user
        quote.save()
        return HttpResponseRedirect(reverse("quote-detail", args=(quote.id,)))

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