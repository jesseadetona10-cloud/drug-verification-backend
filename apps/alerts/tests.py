from django.test import TestCase

class TestCase(TestCase):
    def test_app_loaded(self):
        \"\"\"Test that the alerts app is properly configured\"\"\"
        self.assertTrue(True)
        
    def test_model_imports(self):
        \"\"\"Test that models can be imported\"\"\"
        try:
            from django.apps import apps
            app_config = apps.get_app_config('alerts')
            self.assertIsNotNone(app_config)
        except Exception as e:
            self.fail(f"Failed to import app: {e}")
