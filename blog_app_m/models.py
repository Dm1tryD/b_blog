from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateField(auto_now_add=True)
    date_change = models.DateField(auto_now=True)


    def __str__(self):
        return '{}'.format(self.title)
