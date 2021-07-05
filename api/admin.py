from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

from . import models


# ثبت مدل یوزر
@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', ]
    readonly_fields = ["id", ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Permissions'), {'classes': ('collapse',), 'fields': ('is_active', 'is_staff', 'is_superuser',
                                                                 'groups', 'user_permissions')}),
        (_('Important dates'), {'classes': ('collapse',), 'fields': ('last_login', 'date_joined')}),
        ('تکمیلی', {'fields': ('mobile',)}),
    )


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'shamse_date', 'ProfitCalculate', 'created']
    ordering = ['created']
    list_filter = ['user']

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as exp:
            messages.error(request, exp)
            return


@admin.register(models.ProfitCalculate)
class ProfitCalculateAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', ]
    readonly_fields = ['transaction']


admin.site.register(models.Post)
# admin.site.register(models.Transaction)
