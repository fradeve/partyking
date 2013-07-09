from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

import urllib
import simplejson

fbgraphurl = 'https://graph.facebook.com/'

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(null=True, blank=True, default=0)
    fbid = models.CharField(null=True, max_length=50)
    firstname = models.CharField(null=True, blank=True, max_length=50)
    lastname = models.CharField(null=True, blank=True, max_length=50)
    picture = models.CharField(null=True, blank=True, max_length=50)
    voted = models.IntegerField(null=True, blank=True, default=0)

def fbuserdict(sender, instance, created, **kwargs):
    if created:
        api_query = urllib.request.urlopen(fbgraphurl + str(instance.fbid))
        json = simplejson.loads(api_query.read().decode('utf-8'))
        instance.firstname = json['first_name']
        instance.lastname= json['last_name']
        instance.picture = fbgraphurl + str(instance.fbid) + '/picture'
        instance.save()

signals.post_save.connect(fbuserdict, sender=Profile)
