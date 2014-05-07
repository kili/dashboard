from django.conf import settings
from django.utils import importlib
import warnings


class CustomizationLoader:
    customization_classes = []

    def __init__(self):
        try:
            configured_customizations = getattr(settings, 'CUSTOMIZATIONS')
        except AttributeError:
            warnings.warn('CUSTOMIZATIONS is not configured in settings')

        for customization in configured_customizations:
            bits = customization.split('.')
            if len(bits) == 1:
                raise ValueError('Importing a local function as string is '
                                 'not supported')
            try:
                mod = importlib.import_module('.'.join(bits[:-1]))
            except ImportError:
                raise ImportError('The module %s could not be imported' %
                                  '.'.join(bits[:-1]))
            try:
                self.customization_classes.append(getattr(mod, bits[-1]))
            except AttributeError:
                raise ValueError('The module %s has no class %s' %
                                 ('.'.join(bits[:-1]), bits[-1]))

    def execute(self):
        """Call the execute method on all loaded customization objects."""
        for obj in self.customization_classes:
            obj().execute()

CustomizationLoader().execute()
