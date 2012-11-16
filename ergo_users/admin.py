from django.contrib import admin
from ergo_users.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('ergo_id',)
    
admin.site.register(UserProfile, UserProfileAdmin)
