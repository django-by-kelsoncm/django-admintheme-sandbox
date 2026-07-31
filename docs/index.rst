Django AdminTheme Sandbox
=========================

.. image:: https://img.shields.io/badge/django-6.0-blue.svg
   :target: https://www.djangoproject.com/
   :alt: Django Versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

Pacote Django para ambiente de teste e referência de temas administrativos Django (AdminTheme Sandbox).

📋 Sobre
--------

O **django-admintheme-sandbox** fornece uma biblioteca e estrutura de referência para personalização do Django Admin e formulários Django.

🚀 Instalação
-------------

.. code-block:: bash

   pip install django-admintheme-sandbox

⚙️ Configuração
---------------

1. Adicione ao INSTALLED_APPS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   INSTALLED_APPS = [
       'admintheme_sandbox.apps.AdminThemeSandboxConfig',
       'admintheme_sandbox.apps.AdminThemeSandboxAdminConfig',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]

2. Configure os Context Processors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
                   'admintheme_sandbox.context_processors.layout_settings',
               ],
           },
       },
   ]

3. Colete os Arquivos Estáticos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python manage.py collectstatic

.. toctree::
   :maxdepth: 2
   :caption: Conteúdo:

   start-guide
   contribute
   publishing

📝 Licença
----------

Este projeto está licenciado sob a Licença MIT.
