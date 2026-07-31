from django.utils.translation import gettext as _
from django.http import HttpRequest
from import_export.admin import ImportExportMixin, ExportActionMixin

from admintheme_sandbox.admin import AdminThemeSandboxBaseModelAdmin, ObjectToolSpec


class AdminThemeSandboxModelAdmin(ImportExportMixin, ExportActionMixin, AdminThemeSandboxBaseModelAdmin):

    def get_object_tool_actions(self, request: HttpRequest) -> list[ObjectToolSpec]:
        return super().get_object_tool_actions(request) + [
            ObjectToolSpec(
                label=_("Import"),
                handler="import",
                css_class="import-link",
                permission=f"{self.opts.app_label}.change_{self.opts.model_name}",
                admin=self,
            ),
            ObjectToolSpec(
                label=_("Export"),
                handler="export",
                css_class="export-link",
                permission=f"{self.opts.app_label}.change_{self.opts.model_name}",
                admin=self,
            ),
        ]


DSGovBrModelAdmin = AdminThemeSandboxModelAdmin
