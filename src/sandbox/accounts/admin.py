from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admintheme_sandbox.admin.import_export import AdminThemeSandboxModelAdmin as DSGovBrModelAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(DSGovBrModelAdmin, UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Informações Adicionais (GovBR)", {"fields": ("cargo", "orgao")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações Adicionais (GovBR)", {"fields": ("cargo", "orgao")}),
    )
