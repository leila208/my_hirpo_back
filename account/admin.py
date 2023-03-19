from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.views import PasswordResetView
from .forms import UserAdminCreationForm, UserAdminChangeForm, MyUserPasswordResetForm
from django.urls import path
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
# Register your models here.

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = MyUserPasswordResetForm
    password_reset_template = 'admin/password_reset_form.html'
    
    list_display = ('email', 'name', 'surname', 'is_active', 'is_superuser',
                    'activation_code', 'slug', 'password_reset_code')
    list_filter = ('is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname', 'password','slug')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','company_name','name','surname', 'password1', 'password2')}
        ),
    )
    readonly_fields = ('timestamp','slug',)
    search_fields = ('email', 'name', 'surname')
    ordering = ('timestamp',)
    filter_horizontal = ()
    
    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('password_reset/', PasswordResetView.as_view(
                template_name=self.password_reset_template,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt'
            ), name='admin_password_reset')
        ]
        return urls
admin.site.register(User, UserAdmin)



