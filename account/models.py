from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model) : 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to = 'photos/%Y/%m/', blank=True, null=True, default='default.png')
    bio = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self) : 
        return self.username

    #   overriding save method
    def save(self, *args, **kwargs) : 
        try : 
            prev = UserProfile.objects.get(id=self.id)
            if prev.profile_pic != self.profile_pic and prev.profile_pic!='default.png': 
                prev.profile_pic.delete()
        except : 
            pass
        super().save(*args, **kwargs)

    #   overriding the delete method
    def delete(self, *args, **kwargs) : 
        self.profile_pic.delete()
        super().delete(*args, **kwargs)


    

    