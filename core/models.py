from django.db import models
from django.contrib.auth.models import User

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

class Quote(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    public_accessible = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
