from django.db import models
from django.conf import settings

class Motion(models.Model):
    number = models.CharField(max_length=13, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    withdrawn = models.BooleanField(default=False)
    proponent = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    # Time stamps
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    due = models.DateTimeField()
    
    text = models.TextField()
    
    def __unicode__(self):
        return self.number + ': ' + self.title


class Vote(models.Model):
    motion = models.ForeignKey(Motion)
    VOTE_CHOICES = (
                    (True, 'Aye'),
                    (False, 'Naye'),
                    (None, 'Abstain'),
                   )
    vote = models.NullBooleanField(choices=VOTE_CHOICES)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    certificate = models.TextField(editable=False)
    
    def __unicode__(self):
        return self.motion.number + ': ' + \
               self.get_vote_display() + ' from ' + \
               self.voter.first_name

class ProxyVote(Vote):
    proxy = models.ForeignKey(settings.AUTH_USER_MODEL)
    justification = models.TextField()
    
    def __unicode__(self):
        return super(ProxyVote, self).__unicode__() + ' via ' + self.proxy.first_name