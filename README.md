# Django AdminTheme Sandbox 🏛️

[![Python Versions](https://img.shields.io/pypi/pyversions/django-admintheme-sandbox.svg)](https://pypi.org/project/django-admintheme-sandbox/)
[![Django Versions](https://img.shields.io/badge/django-6.0-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pacote Django para ambiente de sandbox e referência de temas administrativos no Django Admin e formulários Django.

---

## Sobre

O **django-admintheme-sandbox** facilita a implementação e teste de temas administrativos em projetos Django, garantindo conformidade visual, reutilização de componentes e ambiente de demonstração completo.

---

## Como Usar

### 1. Instalação via pip

```bash
pip install django-admintheme-sandbox
```

### 2. Configuração no `settings.py`

Adicione as configurações da aplicação ao seu `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'admintheme_sandbox.apps.AdminThemeSandboxConfig',
    'admintheme_sandbox.apps.AdminThemeSandboxAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ...
]
```

---

## Desenvolvimento Local

```bash
# Sincronizar dependências com uv
uv sync

# Rodar os testes
pytest
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.
