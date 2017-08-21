from django.db import models

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

    class Meta:
        ordering = ("name",)

