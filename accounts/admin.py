from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import SchoolUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new accounts. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SchoolUser
        # fields = ('email', 'first_name','last_name','date_of_birth')
        fields = ('email',)


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating accounts. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SchoolUser
        # fields = ('email', 'password', 'first_name','last_name','date_of_birth', 'is_active', 'is_admin', 'is_staff')
        fields = ('email', 'password', 'is_active', 'is_admin', 'is_staff') #  <--- with out Name and DOB


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.


    list_display = ('email', 'is_admin','is_staff')


    list_filter = ('is_admin',)
    readonly_fields = ('created_at','updated_at','last_login')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),


        ('Permissions', {'fields': ('is_admin','is_active','is_staff')}),
        ('Important Dates', {'fields': ('last_login','created_at','updated_at')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),

            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(SchoolUser, UserAdmin)
