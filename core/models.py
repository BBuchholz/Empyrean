from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Fragment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("text",)

class Document(models.Model):
    name = models.CharField(max_length=200)
    link = models.TextField() #in case we have very long parameter based urls
    fragments = models.ManyToManyField(Fragment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('document-detail', args=[str(self.id)])

    class Meta:
        ordering = ("name",)


class SourceType(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

class Source(models.Model):    
    source_type = models.ForeignKey(SourceType, on_delete=models.PROTECT)
    author = models.TextField()
    director = models.TextField()
    title = models.TextField()
    year = models.TextField()
    url = models.TextField()
    retrieval_date = models.TextField()
    source_tag= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        if title:
            return title
        elif author:
            return author
        elif director:
            return director
        elif year:
            return year
        elif url:
            return url
        else:
            return "undefined source"

    class Meta:
        ordering = ("title", "author", "director", "year", "url",)

class MediaTag(models.Model):
    tag = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ("tag",)

class SourceExcerpt(models.Model):
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    content = models.TextField()
    pages = models.TextField()
    begin_time = models.TextField()
    end_time = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(MediaTag, through='SourceExcerptTagging')

    def __str__(self):
        return self.content

    class Meta:
        ordering = ("content", "pages", "begin_time", "end_time",)

class SourceExcerptTagging(models.Model):
    excerpt = models.ForeignKey(SourceExcerpt, on_delete=models.CASCADE)
    tag = models.ForeignKey(MediaTag, on_delete=models.CASCADE)
    tagged_at = models.DateTimeField(null=True, blank=True)
    untagged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    text = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(default=datetime.now)
    public_accessible = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)    
    tags = models.ManyToManyField(MediaTag, through='QuoteTagging')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('quote-detail', args=[str(self.id)])

    @property
    def is_public(self):
        #just an adaptation of a basic example from the tutorial
        #using properties in templates
        if public_accessible:
            return public_accessible
        else:
            return False

class QuoteTagging(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    tag = models.ForeignKey(MediaTag, on_delete=models.CASCADE)
    tagged_at = models.DateTimeField(null=True, blank=True)
    untagged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


