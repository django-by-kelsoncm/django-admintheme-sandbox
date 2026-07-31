import os
import re
from compressor.filters import FilterBase


class ES6BundlerFilter(FilterBase):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content, *args, **kwargs)

    def input(self, **kwargs):
        if not self.filename:
            return self.content

        bundled_files = set()
        bundle_content = []

        def bundle_file(filepath):
            filepath = os.path.abspath(filepath)
            if filepath in bundled_files:
                return
            bundled_files.add(filepath)

            if not os.path.exists(filepath):
                if not filepath.endswith(".js"):
                    filepath += ".js"
                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"Could not find imported file: {filepath}")

            dirname = os.path.dirname(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            imports = re.findall(
                r'import\s+(?:[\w\s{},*]+from\s+)?[\'"]([^\'"]+)[\'"]', content
            )

            for imp in imports:
                if imp in ("focus-visible", "flatpickr", "@popperjs/core"):
                    continue
                if imp.startswith("."):
                    imp_path = os.path.join(dirname, imp)
                    bundle_file(imp_path)

            lines = content.splitlines()
            clean_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("import "):
                    continue

                if stripped.startswith("export default "):
                    line = re.sub(r"^export\s+default\s+", "", line)
                elif stripped.startswith("export "):
                    if not stripped.startswith("export {"):
                        line = re.sub(r"^export\s+", "", line)

                clean_lines.append(line)

            file_content = "\n".join(clean_lines)

            file_content = re.sub(
                r'import\s+\{\s*createPopper\s*\}\s+from\s+[\'"]@popperjs/core[\'"]',
                "const createPopper = window.Popper ? window.Popper.createPopper : null;",
                file_content,
            )
            file_content = re.sub(
                r'import\s+flatpickr\s+from\s+[\'"]flatpickr[\'"]',
                "const flatpickr = window.flatpickr;",
                file_content,
            )

            file_content = re.sub(r"export\s*\{[^}]*\}", "", file_content)

            bundle_content.append(file_content)

        bundle_file(self.filename)
        return "\n".join(bundle_content)
