from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'is_employer', 'is_active', 'is_staff']
    list_filter = ['email', 'is_staff', 'is_active', 'is_superuser', 'is_employer']
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_employer')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_employer', 'is_staff', 'is_active')}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)