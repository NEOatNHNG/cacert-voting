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
    list_display = ('number', 'title',)
    list_filter = ('created', 'due',)
    search_fields = ('title', 'text', 'number')

admin.site.register(Motion, MotionAdmin)