from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class AdminThemeSandboxConfig(AppConfig):
    name: str = "admintheme_sandbox"
    verbose_name: str = "AdminTheme Sandbox"
    icon: str = "fa fa-edit"

    def ready(self):
        from admintheme_sandbox.menus import autodiscover

        autodiscover()


class AdminThemeSandboxAdminConfig(AdminConfig):
    """
    Herdar de AdminConfig garante que o Django execute o autodiscover()
    e encontre todos os arquivos admin.py do projeto automaticamente.
    """

    default_site = "admintheme_sandbox.admin.AdminThemeSandboxAdminSite"
