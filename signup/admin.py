from django.contrib import admin
from signup.models import SignupQueue, Contact, AccessRight


class QueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'organization', 'email', 'status')

admin.site.register(SignupQueue, QueueAdmin)
admin.site.register(Contact)
admin.site.register(AccessRight)
