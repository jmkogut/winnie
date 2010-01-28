from potbotadmin.Test.models import *
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
	list_display = ('email', 'can_create', 'can_update', 'can_delete')
	list_filter = ('can_create', 'can_update', 'can_delete')

class PhraseAdmin(admin.ModelAdmin):
	list_display = ('response', 'category', 'enabled')
	list_filter = ('category', 'enabled')

class IntelligenceAdmin(admin.ModelAdmin):
	list_display = ('nick', 'keyphrase', 'indicator', 'value')
	list_filter = ('indicator',)
	search_fields = ('keyphrase', 'indicator', 'value')

admin.site.register(Account, AccountAdmin)
admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Intelligence, IntelligenceAdmin)
