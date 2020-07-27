from django import forms
from django.contrib import admin
from .models import Content, User
# from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re

def UppercaseLowercaseValidator(value):
    if not re.findall('[A-Z]', value):
        raise ValidationError(_("The password must contain at least 1 uppercase letter, A-Z."))
    elif not re.findall('[a-z]', value):
        raise ValidationError(_("The password must contain at least 1 lowercase letter, a-z."))

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    phone_number = forms.CharField(max_length=10)
    pincode = forms.CharField(max_length=6)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[UppercaseLowercaseValidator])
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput,
                                validators=[UppercaseLowercaseValidator])

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'pincode')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        # UppercaseValidator.validate(self.cleaned_data.get('password1'),None)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'pincode', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # model = User
    list_display = ('email', 'is_staff', 'is_active','first_name', 'last_name')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name', 'last_name', 'phone_number', 'pincode')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'pincode',
                       'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

admin.site.register(Content)
