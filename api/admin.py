from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin
from import_export.admin import ImportExportModelAdmin

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


class TarakoneshInline(admin.TabularInline):
    model = models.Tarakonesh

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.Ashkhas)
class AshkasAdmin(ImportExportModelAdmin):
    list_display = ['id', '__str__', 'Moaref_Tbl_Ashkhas_id', 'Mizan_Har_Melyoon',]
    list_filter = ['Moaref_Tbl_Ashkhas_id', ]
    search_fields = ['id', 'Lname']
    ordering = ['id']
    inlines = [TarakoneshInline]


@admin.register(models.Tarakonesh)
class TarakoneshAdmin(ImportExportModelAdmin):
    list_display = ['__str__', 'shakhs', 'tarikh', 'kind', 'Mablagh', ]
    list_filter = ['kind', 'date_time', ]
    search_fields = ['shakhs__Lname', ]


@admin.register(models.TransactionKind)
class TarakoneshAdmin(ImportExportModelAdmin):
    pass


admin.site.register(models.Post)
# admin.site.register(models.TransactionKind)
# admin.site.register(models.Transaction)
