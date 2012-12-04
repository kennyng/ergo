from django.contrib import admin
from ergo_users.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname',)
    readonly_fields = ('ergo_id',)
    search_fields = ['firstname', 'lastname']
    
admin.site.register(UserProfile, UserProfileAdmin)
