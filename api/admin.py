from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.utils.translation import ugettext_lazy as _
# you need import this for adding jalali calander widget
from import_export.admin import ImportExportModelAdmin

from . import models


# from simple_history.admin import SimpleHistoryAdmin


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


@admin.register(models.Transaction_old)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'shamse_date', ]
    list_filter = ['user']

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as exp:
            messages.error(request, exp)
            return


@admin.register(models.ProfitCalculate)
class ProfitCalculateAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]
    readonly_fields = ['transaction']


class TarakoneshInline(admin.TabularInline):
    model = models.Transaction

    def has_change_permission(self, request, obj=None):
        return False


class ImageTabularInlineAdmin(GenericStackedInline):
    model = models.Image
    ct_field = "content_type"
    ct_fk_field = "object_id"


class ProfileImageGalleryInline(admin.StackedInline):
    model = models.ProfileImageGallery
    inlines = [ImageTabularInlineAdmin]


@admin.register(models.Profile)
class AshkasAdmin(ImportExportModelAdmin):
    list_display = ['id', '__str__', 'presenter', 'percent', 'state', ]
    list_filter = ['presenter', ]
    search_fields = ['id', 'last_name']
    ordering = ['id']
    # inlines = [ProfileImageGalleryInline]
    inlines = [ImageTabularInlineAdmin]


@admin.register(models.Transaction)
class TarakoneshAdmin(admin.ModelAdmin):
    list_display = ['profile', 'kind', 'amount', 'state', ]
    list_filter = ['kind', 'date_time', 'state', ]
    search_fields = ['id', ]


# @admin.register(models.Pelekan)
# class TarakoneshAdmin(SimpleHistoryAdmin):
#     list_display = ["id", "az", "ta","__str__"]
#     # history_list_display = ["status"]

@admin.register(models.Pelekan)
class PelekanAdmin(admin.ModelAdmin):
    list_display = ["id", "az", "ta", "__str__"]
    list_filter = ['kind', ]
    # history_list_display = ["status"]


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'duration', 'every_n_months']


@admin.register(models.TransactionKind)
class TransactionKindAdmin(ImportExportModelAdmin):
    pass


admin.site.register(models.Post)
admin.site.register(models.ImageKind)
admin.site.register(models.ProfitKind)
# admin.site.register(models.Plan)
admin.site.register(models.ProfileImageGallery)
admin.site.register(models.TransactionRequest)
admin.site.register(models.TransactionRequestKind)
admin.site.register(models.Bank)
# admin.site.register(models.Transaction_old)
