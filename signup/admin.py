from django.contrib import admin
from signup.models import SignupQueue

class QueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'organization', 'email', 'city')

admin.site.register(SignupQueue, QueueAdmin)