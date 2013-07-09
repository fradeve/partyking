from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from partyking.apps.core.models import Profile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ExtentedInline(admin.StackedInline):
    model = Profile
    can_delete = False
    exclude = ('picture', 'firstname', 'lastname')

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ExtentedInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)