from django.contrib import admin
from core.models import (
    Fragment, 
    Document, 
    Quote, 
    MediaTag, 
    QuoteTagging, 
    Source, 
    SourceExcerpt,
    SourceExcerptTagging,
    SourceType,
)


# Register your models here.
admin.site.register(Fragment)
admin.site.register(Document)
#admin.site.register(Quote) #registered below 
admin.site.register(MediaTag)
admin.site.register(QuoteTagging)
admin.site.register(Source)
admin.site.register(SourceExcerpt)
admin.site.register(SourceExcerptTagging)
admin.site.register(SourceType)


# register admin classes for Quote with the decorator
@admin.register(Quote) 
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'public_accessible')








