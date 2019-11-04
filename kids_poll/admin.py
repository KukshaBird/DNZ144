from django.contrib import admin

from .models import Poll, Item, Vote


class PollItemInline(admin.TabularInline):
    model = Item
    extra = 0
    max_num = 15


class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'vote_count', 'is_published')
    inlines = [PollItemInline,]


class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'ip', 'kid', 'created_at')
    list_filter = ('poll', 'kid', 'created_at')

# registration in admin
admin.site.register(Vote, VoteAdmin)
admin.site.register(Poll, PollAdmin)