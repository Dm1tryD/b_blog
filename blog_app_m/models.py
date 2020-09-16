from django.db import models
from django.shortcuts import reverse

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateField(auto_now_add=True)
    date_change = models.DateField(auto_now=True)

    def get_absolute_url(self):
        """Returns the generated url link"""
        return reverse('post_detail_url',kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,unique=True)

    def get_absolute_url(self):
        """Returns the generated url link"""
        return reverse('tag_detail_url',kwargs={'slug':self.slug})

    def __str__(self):
        return self.title