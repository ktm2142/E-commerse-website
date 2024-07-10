from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'email', 'city', 'truncated_address')
    # list_filter = ('phone_number',)
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_number', 'email', 'city', 'address')

    def truncated_address(self, obj):
        if len(obj.address) > 20:
            return obj.address[:20] + '...'
        return obj.address
    truncated_address.short_description = 'Address'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
