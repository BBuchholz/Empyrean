from django.contrib import admin
from core.models import Fragment, Document, Quote

# Register your models here.
admin.site.register(Fragment)
admin.site.register(Document)
#admin.site.register(Quote) #registered below 

# register admin classes for Quote with the decorator
@admin.register(Quote) 
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'public_accessible')