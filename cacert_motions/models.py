from django.db import models
from django.conf import settings

class Motion(models.Model):
    number = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=255)
    withdrawn = models.BooleanField(default=False)
    proponent = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    # Time stamps
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    due = models.DateTimeField()
    
    text = models.TextField()


class Vote(models.Model):
    motion = models.ForeignKey(Motion)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL)
    VOTE_CHOICES = (
                    (True, 'Aye'),
                    (False, 'Naye'),
                    (None, 'Abstain'),
                   )
    vote = models.NullBooleanField(choices=VOTE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    certificate = models.TextField()

class ProxyVote(Vote):
    proxy = models.ForeignKey(settings.AUTH_USER_MODEL)
    justification = models.TextField()