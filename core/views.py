from django.shortcuts import render
from django.http import HttpResponse
from .models import Fragment, Document

def index(request):
    #return HttpResponse("Nine Worlds Deep")

    # adapting from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page

    # counts 
    num_frags = Fragment.objects.all().count()
    num_docs = Document.objects.all().count()

    # render
    return render(
    	request,
    	'index.html',
    	context={'num_frags':num_frags, 'num_docs':num_docs},
    )

