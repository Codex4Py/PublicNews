from django.contrib import admin
from .models import NewsPost, Category, SocialMediaLink, Contact, CustomUser, Comment

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    
    # Add fieldsets for detailed user edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add fields to the user creation page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models without a custom admin class
admin.site.register(NewsPost)
admin.site.register(Category)
admin.site.register(SocialMediaLink)
admin.site.register(Contact)
admin.site.register(Comment)
