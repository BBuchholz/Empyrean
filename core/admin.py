from django.contrib import admin
from core.models import Fragment, Document, Quote
from core.models import QuoteAccessLogEntry

# Register your models here.
admin.site.register(Fragment)
admin.site.register(Document)
#admin.site.register(Quote) #registered below 
admin.site.register(QuoteAccessLogEntry)

# register admin classes for Quote with the decorator
@admin.register(Quote) 
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'public_accessible')