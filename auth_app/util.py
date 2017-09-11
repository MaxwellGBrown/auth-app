import threading


def sub_settings(settings, sub_key=None, delimiter='.'):
    """
    k: v from config where key.startswith(sub_key) separated by delimiter
    """
    prefix = sub_key + delimiter
    return {
        k[len(prefix):]: v for k, v in settings.items()
        if k.startswith(prefix)
    }


class scoped(object):
    """
    An interface for session-like objects with thread safety

    Based directly off of SQLAlchemy's scoped_session & ThreadLocalRegistry
    """

    factory = None

    def __init__(self, factory):
        self.factory = factory
        self.registry = threading.local()

    def __call__(self):
        """ Return (or create) the current factory-created object """
        try:
            return self.registry.value
        except AttributeError:
            self.registry.value = self.factory()
            return self.registry.value

    def __getattr__(self, key):
        """ Interface with registered value instead of scoped """
        value = self()
        return getattr(value, key)
