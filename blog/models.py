from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime as dt, timedelta

from ckeditor.fields import RichTextField

class Blog(models.Model) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length = 200, blank=True, null=True)
    slug = models.SlugField()
    body = RichTextField()
    cover_pic = models.ImageField(upload_to = 'cover/', blank=True, null=True)
    is_private = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self) : 
        return self.title

    def delete(self, *args, **kwargs) :
        self.cover_pic.delete()
        super().delete(*args, **kwargs)
