from django.utils.importlib import import_module
from django.conf import settings
import warnings


class CustomizationLoader:

    def __init__(self):
        try:
            self.customizations = getattr(settings, 'CUSTOMIZATIONS')
        except AttributeError:
            warnings.warn('CUSTOMIZATIONS is not configured in settings')

    def load(self):
        """
        load all the configured customizations and call the execute()
        method on them
        """
        for customization in self.customizations:
            bits = customization.split('.')
            if len(bits) == 1:
                raise ValueError('Importing a local function as string is '
                                 'not supported')
            try:
                mod = import_module('.'.join(bits[:-1]))
            except ImportError:
                raise ImportError('The module %s could not be loaded' %
                                  '.'.join(bits[:-1]))
            try:
                obj = getattr(mod, bits[-1])
            except AttributeError:
                raise ValueError('The module %s has no class %s' %
                                 ('.'.join(bits[:-1]), bits[-1]))
            obj().execute()

CustomizationLoader().load()
