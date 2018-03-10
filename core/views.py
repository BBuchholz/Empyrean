from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from .models import Fragment, Document, Quote, QuoteAccessLogEntry
from .models import Fragment, Document, Quote, SourceType, Source, MediaTag, QuoteTagging
from .forms import QuoteForm
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

from django.contrib.auth.decorators import login_required

import xml.etree.ElementTree as ET


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
    
    #ensure the existence of default source and tag
    source_type, created = SourceType.objects.get_or_create(
        name='UNSPECIFIED',
    )

    Source.objects.get_or_create(
        source_type=source_type,
        author='UNSPECIFIED SOURCE',
    )

    media_tag_needs_tagging, created = MediaTag.objects.get_or_create(
        tag='needs tagging',
    )

    media_tag_empyrean_system_tagged, created = MediaTag.objects.get_or_create(
        tag='empyrean system tagged',
    )


    #these numbers are for testing, increase when working
    num_quotes_to_retrieve = 10
    num_quotes_to_randomize = 5

    if request.user.is_authenticated:

        # grab X quotes, select where public_accessible is true or owner is logged in user
        quote_queryset = Quote.objects.filter(Q(owner=request.user)|Q(public_accessible=True)).order_by("last_accessed")[:num_quotes_to_retrieve]
        pass

    else:

        # grab X publicly accessible quotes, select from most recent by id
        quote_queryset = Quote.objects.filter(public_accessible=True).order_by("last_accessed")[:num_quotes_to_retrieve]

    # take retrieved quotes and randomize to grab Y quotes and add to variable random_quotes
    quote_list = random.sample(list(quote_queryset), num_quotes_to_randomize)

    # just passing a list of what we need from each object, instead of the whole object to the template
    quote_list_simple = []


    for quote in quote_list:
        quote.last_accessed = datetime.now()
        quote.save()
        quote_text = quote.text
        
        if quote.source:
            quote_source_text = str(quote.source)
        else:
            quote_source_text = "[no source found]"
       
        quote_tags_values_list = quote.tags.values_list('tag', flat=True)

        if len(quote_tags_values_list) < 1:
            quote_tagging = QuoteTagging(quote=quote, tag=media_tag_needs_tagging, tagged_at=datetime.now())
            quote_tagging.save()
            quote_tagging = QuoteTagging(quote=quote, tag=media_tag_empyrean_system_tagged, tagged_at=datetime.now())
            quote_tagging.save()
            quote_tags_values_list = quote.tags.values_list('tag', flat=True)

        if len(quote_tags_values_list) > 0:
            quote_tag_string = ", ".join(quote_tags_values_list)
        else:
            quote_tag_string = ", ".join('tags', 'not', 'found', 'here',)

        quote_list_simple.append((quote_text, quote_source_text, quote_tag_string))
        


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
            'quote_list_simple': quote_list_simple,
        },
    )

# @login_required
# def quote_entry(request):
#     #if its a post request, process the data
#     if(request.method == 'POST'):
        
#         #create form instance and populate with data from the request
#         form = QuoteForm(request.POST)

#         #check form validity
#         if form.is_valid():
#             #proces the data in form.cleaned_data
#             quote = Quote()
#             quote.text = form.cleaned_data['quote_text']
#             quote.public_accessible = form.cleaned_data['public_accessible']
#             quote.owner = request.user
#             quote.save()

#             return HttpResponseRedirect(reverse('my-quotes'))

#     #if this is a GET (or any other method) create the default form
#     else:

#         form = QuoteForm()

#     return render(request, 'core/')

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
    form_class = QuoteForm

    def form_valid(self, form):
        quote = form.save(commit=False)
        quote.owner = self.request.user
        quote.save()
        
        #unable to actually save tags on entry (prompt exists but QuoteTaggings will not save)
        #tried using save_m2m(), but current implementation will not work using save_m2m() 
        #because of the intermediary model (google it)
        #saving this for later, because we may be onto something ->
        #try combining this solution: https://stackoverflow.com/a/10249376/670768
        #and this solution: https://stackoverflow.com/a/2264722/670768

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

def xml_download(request):
    #reference: https://stackoverflow.com/questions/45979406/serve-dynamically-generated-xml-file-to-download-in-django-with-character-encodi
    response = HttpResponse(get_xml(request), content_type="application/xml")
    response['Content-Disposition'] = 'inline; filename=myfile.xml'
    return response

def get_xml(request):

    nwd = ET.Element("nwd")
    
    if request.user.is_authenticated:
        #create doc here 
        archivist_subset = ET.SubElement(nwd, "archivistSubset")
        
        for source in Source.objects.all():

            source = ET.SubElement(archivist_subset, 
                                   "source", 
                                   type=source.source_type.name,
                                   author=source.author,
                                   director=source.director,
                                   title=source.title,
                                   year=source.year,
                                   url=source.url,
                                   retrievalDate=source.retrieval_date,
                                   tag=source.source_tag)

    else:
        msg = ET.SubElement(nwd, "msg", value="user not authenticated")

    xml_string = ET.tostring(nwd, 'utf-8')
    return xml_string.decode('utf-8')