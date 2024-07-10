from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'body', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'body')
    list_filter = ('sender', 'receiver', 'timestamp')
    ordering = ('-timestamp',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sender = request.user
        obj.save()


admin.site.register(Message, MessageAdmin)
