from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from .models import Fragment, Document, Quote, QuoteAccessLogEntry
from .models import Fragment, Document, Quote, SourceType, Source, MediaTag, QuoteTagging, SourceExcerpt
from .forms import QuoteForm
from django.contrib.auth.models import User
from django import forms

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
import random
from datetime import datetime
import pytz

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

    if len(quote_queryset) > num_quotes_to_randomize:

        # take retrieved quotes and randomize to grab Y quotes and add to variable random_quotes
        quote_list = random.sample(list(quote_queryset), num_quotes_to_randomize)

    else:

        quote_list = quote_queryset

    # just passing a list of what we need from each object, instead of the whole object to the template
    quote_list_simple = []


    for quote in quote_list:
        quote.last_accessed = timezone.now()
        quote.save()
        quote_text = quote.text
        
        if quote.source:
            quote_source_text = str(quote.source)
        else:
            quote_source_text = "[no source found]"



        ######### working on alternative ###
        ####################################
        #
        # old code, that (erroneously) includes untagged tag values, comment this out when code below is working
        quote_tags_values_list = quote.tags.values_list('tag', flat=True)

        
        ####################################
        #
        # new code (comment out above when working)
        quote_tags_values = []

        for quote_tagging in quote.quotetagging_set.all():

            testing = False

            if testing:

                quote_tagged_at = str(quote_tagging.tagged_at)
                quote_untagged_at = str(quote_tagging.untagged_at)
                quote_tag_value = str(quote_tagging.tag.tag)

                output_test = quote_tag_value + "-> tagged: "
                output_test += quote_tagged_at + " untagged: "
                output_test += quote_untagged_at
                quote_tags_values.append(output_test)

            else:

                tagged_at = quote_tagging.tagged_at
                untagged_at = quote_tagging.untagged_at

                if untagged_at is not None:

                    if (tagged_at is not None and
                        tagged_at == max(tagged_at, untagged_at)):

                        quote_tags_values.append(str(quote_tagging.tag.tag))

                else:

                    quote_tags_values.append(str(quote_tagging.tag.tag))


        quote_tags_values_list = quote_tags_values

        #
        #
        ####################################
        ######### end of alternative work ###


        if len(quote_tags_values_list) < 1:
            
            # quote_tagging, quote_tagging_created = QuoteTagging.objects.get_or_create(quote=quote, tag=media_tag_needs_tagging)
            # quote_tagging.tagged_at=timezone.now()
            # quote_tagging.save()

            # quote_tagging, quote_tagging_created = QuoteTagging.objects.get_or_create(quote=quote, tag=media_tag_empyrean_system_tagged)
            # quote_tagging.tagged_at=timezone.now()
            # quote_tagging.save()

            # quote_tags_values_list = quote.tags.values_list('tag', flat=True)      
            pass      

        if len(quote_tags_values_list) > 0:
            quote_tag_string = ", ".join(quote_tags_values_list)
        else:
            quote_tag_string = ""

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
    #response['Content-Disposition'] = 'inline; filename=myfile.xml'
    now = timezone.now()
    nwd_timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
    filename = 'nwd_' + nwd_timestamp + '.xml'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    return response

def get_xml(request):

    nwd = ET.Element("nwd")
    
    if request.user.is_authenticated:
        #create doc here 
        archivist_subset_element = ET.SubElement(nwd, "archivistSubset")
        
        for source in Source.objects.all():

            source_element = ET.SubElement(archivist_subset_element, 
                                           "source", 
                                           type=source.source_type.name,
                                           author=source.author,
                                           director=source.director,
                                           title=source.title,
                                           year=source.year,
                                           url=source.url,
                                           retrievalDate=source.retrieval_date,
                                           tag=source.source_tag)

            for quote in Quote.objects.filter(source=source):

                source_excerpt_element = ET.SubElement(source_element,
                                                       "sourceExcerpt")

                source_excerpt_value_element = ET.SubElement(source_excerpt_element,
                                                             "sourceExcerptValue").text=quote.text

                for quote_tagging in QuoteTagging.objects.filter(quote=quote):

                    tagged_at_time = quote_tagging.tagged_at
                    untagged_at_time = quote_tagging.untagged_at

                    tagged_at_string = ""
                    untagged_at_string = ""

                    if tagged_at_time:
                        tagged_at_string = tagged_at_time.strftime('%Y-%m-%d %H:%M:%S')

                    if untagged_at_time:
                        untagged_at_string = untagged_at_time.strftime('%Y-%m-%d %H:%M:%S')

                    tag_element = ET.SubElement(source_excerpt_element,
                                                "tag",
                                                tagValue=quote_tagging.tag.tag,
                                                taggedAt=tagged_at_string,
                                                untaggedAt=untagged_at_string)


    else:
        msg = ET.SubElement(nwd, "msg", value="user not authenticated")

    xml_string = ET.tostring(nwd, 'utf-8')
    return xml_string.decode('utf-8')


def xml_upload(request):
    #if request.method == 'POST' and request.FILES['file']:
    if request.method == 'POST':
        
        if not 'file' in request.FILES:
            return render(request, 'core/xml_upload.html', {
                'xml_upload_processed_message': 'choose a file for upload'
            })  

        if not request.user.is_authenticated:
            return render(request, 'core/xml_upload.html', {
                'xml_upload_processed_message': 'must be logged in to upload xml'
            })  

        file = request.FILES['file']
        context = process_xml_upload(request)
        return render(request, 'core/xml_upload.html', context)

    return render(request, 'core/xml_upload.html')

def process_xml_upload(request):
    file = request.FILES['file']
    uploaded_file_name = file.name

    sources_processed = 0
    source_location_subset_entries_processed = 0
    source_excerpts_processed = 0
    source_excerpt_annotations_processed = 0
    tags_processed = 0

    try:
        tree = ET.parse(file)
        root = tree.getroot()

        for source in root.iter('source'):

            source_type_value = source.get('type')
            author = source.get('author')
            director = source.get('director')
            title = source.get('title')
            year = source.get('year')
            url = source.get('url')
            retrieval_date = source.get('retrievalDate')
            source_tag = source.get('tag')

            source_type, source_type_created = SourceType.objects.get_or_create(
                name=source_type_value,
            )

            source_object, created = Source.objects.get_or_create(
                source_type = source_type,
                author = author,
                director = director,
                title = title,
                year = year,
                url = url,
                retrieval_date = retrieval_date,
                source_tag = source_tag,
            )

            for source_location_subset_entries in source.findall('sourceLocationSubsetEntry'):

                location = source_location_subset_entry.get('location')
                location_subset = source_location_subset_entry.get('locationSubset')
                location_subset_entry = source_location_subset_entry.get('locationSubsetEntry')
                verified_present = source_location_subset_entry.get('verifiedPresent')
                verified_missing = source_location_subset_entry.get('verifiedMissing')

                # Empyrean V5 only storing source, source_excerpt(as Quote), and tags(as QuoteTagging)...
                # values are still read here because V6 will store everything

                source_location_subset_entries_processed += 1

            for source_excerpt in source.findall('sourceExcerpt'):

                source_excerpt_value = source_excerpt.find('sourceExcerptValue').text
                pages = source_excerpt.get('pages')
                begin_time = source_excerpt.get('beginTime')
                end_time = source_excerpt.get('endTime')

                quote_object, quote_created = Quote.objects.get_or_create(
                    source=source_object,
                    text=source_excerpt_value,
                )

                if quote_created:
                    quote_object.public_accessible = False
                    quote_object.owner = request.user
                    quote_object.save()

                for source_excerpt_annotation in source_excerpt.findall('SourceExcerptAnnotation'):

                    source_excerpt_annotation_value = source_excerpt_annotation.find('SourceExcerptAnnotationValue')
                    linked_at = source_excerpt_annotation.get('linkedAt')
                    unlinked_at = source_excerpt_annotation.get('unlinkedAt')

                    # Empyrean V5 only storing source, source_excerpt(as Quote), and tags(as QuoteTagging)...
                    # values are still read here because V6 will store everything

                    source_excerpt_annotations_processed += 1

                for tag in source_excerpt.findall('tag'):

                    tag_value = tag.get('tagValue')
                    tagged_at = tag.get('taggedAt')
                    untagged_at = tag.get('untaggedAt')                    

                    tag_object, tag_created = MediaTag.objects.get_or_create(
                        tag=tag_value,
                    )

                    quote_tagging, quote_tagging_created = QuoteTagging.objects.get_or_create(
                        quote=quote_object, 
                        tag=tag_object,
                    )

                    if quote_tagging_created:
                        # set taggedAt
                        quote_tagging.tagged_at= timezone.now()

                    else:
                        # set tagged_at and untagged_at to more recent of each   
                        if tagged_at :
                            xml_tagged_at_time = datetime.strptime(tagged_at, '%Y-%m-%d %H:%M:%S')
                            # force timezone aware
                            xml_tagged_at_time = pytz.utc.localize(xml_tagged_at_time)
                            
                            if quote_tagging.tagged_at is not None:
                                current_tagged_at_time = quote_tagging.tagged_at
                                quote_tagging.tagged_at = max(xml_tagged_at_time, current_tagged_at_time)
                            else:
                                quote_tagging.tagged_at = xml_tagged_at_time

                        if untagged_at:
                            xml_untagged_at_time = datetime.strptime(untagged_at, '%Y-%m-%d %H:%M:%S')
                            # force timezone aware
                            xml_untagged_at_time = pytz.utc.localize(xml_untagged_at_time)

                            if quote_tagging.untagged_at is not None:
                                current_untagged_at_time = quote_tagging.untagged_at
                                quote_tagging.untagged_at = max(xml_untagged_at_time, current_untagged_at_time)
                            else:
                                quote_tagging.untagged_at = xml_untagged_at_time

                    # either way, save the new timestamps
                    quote_tagging.save()

                    tags_processed += 1

                source_excerpts_processed += 1

            sources_processed += 1


        processed_message = "successfully processed uploaded XML."

    except Exception as e:

        processed_message = "unexpected error processing xml [" + str(e) + "]... aborted."

    #build strings for processed statistics to return
    if sources_processed > 0:
        sources_processed_string = str(sources_processed) + " sources"
    if source_location_subset_entries_processed > 0:
        source_location_subset_entries_processed_string = str(source_location_subset_entries_processed) + " source location subset entries"
    if source_excerpts_processed > 0:
        source_excerpts_processed_string = str(source_excerpts_processed) + " source excerpts"
    if source_excerpt_annotations_processed > 0:
        source_excerpt_annotations_processed_string = str(source_excerpt_annotations_processed) + " source excerpt annotations"
    if tags_processed > 0:
        tags_processed_string = str(tags_processed) + " tags"


    return {'uploaded_file_name': uploaded_file_name,
            'xml_upload_processed_message': processed_message,
            'sources_processed': sources_processed,
            'source_location_subset_entries_processed': source_location_subset_entries_processed,
            'source_excerpts_processed': source_excerpts_processed,
            'source_excerpt_annotations_processed': source_excerpt_annotations_processed,
            'tags_processed': tags_processed
           }



