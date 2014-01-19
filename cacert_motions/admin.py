from django.contrib import admin
from .models import Motion, Vote, ProxyVote

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1
    
    readonly_fields = ('timestamp',)
    fields = (
        ('vote', 'voter', 'timestamp',),
    )

class ProxyVoteInline(admin.TabularInline):
    model = ProxyVote
    
    readonly_fields = ('timestamp',)
    fields = (
        ('vote', 'voter', 'proxy', 'timestamp',),
        'justification'
    )

class MotionAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'created', 'modified',)
    fields = (
        ('number', 'title', 'withdrawn',),
        'proponent',
        ('created', 'modified', 'due',),
        'text',
    )
    
    inlines = (VoteInline, ProxyVoteInline,)
    
    date_hierarchy = 'created'
    list_display = ('approved',
                    'number',
                    'title',
                    'ayes__count',
                    'nays__count',
                    'abstains__count',
                    )
    list_display_links = ('approved',
                          'number',
                          'title',
                          )
    list_filter = ('created', 'due',)
    search_fields = ('title', 'text', 'number')
    
    def ayes__count(self, motion):
        return motion.ayes().count()
    ayes__count.short_description = 'Ayes'
    
    def nays__count(self, motion):
        return motion.nays().count()
    nays__count.short_description = 'Nays'
    
    def abstains__count(self, motion):
        return motion.abstains().count()
    abstains__count.short_description = 'Abstains'

admin.site.register(Motion, MotionAdmin)