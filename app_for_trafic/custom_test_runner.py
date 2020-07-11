from django.test.runner import DiscoverRunner
from django.core import management
from services_mail_server import settings_test


class UnManagedModelTestRunner(DiscoverRunner):

    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        get_models = apps.get_models
        tables_for_creating_fixture = ["{}.{}".format(item._meta.app_label, item._meta.db_table) for item in get_models() if hasattr(item, 'AdditionalAttr') and item.AdditionalAttr.make_fixture]
        management.call_command('dumpdata',
                                *tables_for_creating_fixture,
                                output=settings_test.FIXTURE_FILES,
                                indent=3,
                                natural_foreign=True)
        self.unmanaged_models = [m for m in get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        for m in self.unmanaged_models:
            m._meta.managed = False
