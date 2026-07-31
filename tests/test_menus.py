import pytest
from django.conf import settings
from django.test import RequestFactory
from admintheme_sandbox import menus


@pytest.fixture(autouse=True)
def setup_django():
    if not settings.configured:
        settings.configure(
            SECRET_KEY="test-secret-key",
            ROOT_URLCONF=__name__,
            INSTALLED_APPS=[
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
            ],
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": True,
                }
            ],
        )
    import django

    django.setup()


@pytest.fixture
def request_factory():
    return RequestFactory()


def test_menu_item_creation():
    item = menus.MenuItem("Teste", "/teste/", icon="fa fa-test", order=10)
    assert item.name == "Teste"
    assert item.url == "/teste/"
    assert item.icon == "fa fa-test"
    assert item.order == 10


def test_menu_folder_creation():
    folder = menus.MenuFolder("app_teste", "App Teste", icon="fa fa-folder")
    assert folder.app_label == "app_teste"
    assert folder.name == "App Teste"
    assert folder.icon == "fa fa-folder"


def test_menu_registry_register_folder():
    registry = menus.MenuRegistry()
    folder = registry.register_folder("app1", name="App Um")
    assert folder.name == "App Um"
    assert "app1" in registry._folders


def test_menu_registry_register_item():
    registry = menus.MenuRegistry()
    item = registry.register_item("app1", "Item Um", "/item1/")
    assert item.name == "Item Um"
    assert item.url == "/item1/"
    assert len(registry._folders["app1"]._items) == 1
