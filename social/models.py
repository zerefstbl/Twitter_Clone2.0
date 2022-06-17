from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to='media/post_picture', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_on = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile', verbose_name='user')
    name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    picture = models.ImageField(upload_to='media/profile_pictures', default='media/profile_pictures/default.png', blank=True)
    teste = models.ManyToManyField(User, related_name='teste', blank=True)
    following = models.ManyToManyField(User, blank=True, related_name='following')

    
    def __str__(self):
        return self.user.username
    



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        lal = Profile.objects.create(user=instance)
        print('OOOOOOOOOOOOOOS', lal.pk)
        lal.following.add(lal.pk)
        
        
        


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Notifications(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from', null=True)
    notification_type = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True)
    user_has_seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    
