from django.contrib import admin
from .models import Poll


# Register your models here.


class PollsAdmin(admin.ModelAdmin):
    model = Poll
    readonly_fields = ['start_date']
    fields = ['name', 'end_date', 'description']


admin.register(Poll, PollsAdmin)