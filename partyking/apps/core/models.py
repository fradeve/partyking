__appname__ = "PartyKing"
__author__  = "Francesco de Virgilio (fradeve)"
__license__ = "GNU GPL 3.0 or later"

__version__ = "0.1"

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

import requests

FBGRAPHURL = 'https://graph.facebook.com/'

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(blank=True, default=0)
    fbid = models.CharField(null=True, max_length=50)
    firstname = models.CharField(null=True, blank=True, max_length=50)
    lastname = models.CharField(null=True, blank=True, max_length=50)
    picture = models.URLField(null=True, blank=True, max_length=50)
    voted = models.IntegerField(blank=True, default=0)
    email = models.EmailField(blank=False)

# TODO: add email notification from http://stackoverflow.com/questions/2809547/creating-email-templates-with-django
def sendnotifcation(mailaddress):
    subject, from_email, to = 'Invite from PartyKing!', 'admin@partyking.fradeve.org', str(mailaddress)
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# TODO: move function to save() inside Profile model
def fbuserdict(sender, instance, created, **kwargs):
    if created:
        try:
            api_query = requests.get(FBGRAPHURL + str(instance.fbid))
            try:
                json = api_query.json()
                instance.firstname = json['first_name']
                instance.lastname= json['last_name']
                instance.picture = FBGRAPHURL + str(instance.fbid) + '/picture'
                sendnotifcation(instance.email)
                instance.save()
            except requests.ValueError:
                pass
        except requests.ConnectionError:
            pass

signals.post_save.connect(fbuserdict, sender=Profile)
