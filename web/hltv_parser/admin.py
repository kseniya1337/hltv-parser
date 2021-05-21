from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.utils.translation import ugettext_lazy as _

from hltv_parser.models.user import User


class UserChangeForm(BaseUserChangeForm):

    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm

    fieldsets = [
        (None, {
            'fields': [
                'username',
                'password',
            ],
        }),
        (_('Personal info'), {
            'fields': [
                'first_name',
                'last_name',
                'email',
            ],
        }),
    ]


admin.site.register(User, UserAdmin)