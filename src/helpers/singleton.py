from typing import ClassVar


class Singleton:
    _singleton: ClassVar = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            return object.__new__(cls)
        raise RuntimeError(
            'A singleton instance already exists, use get_instance() instead.')

    @classmethod
    def get_instance(cls) -> 'Singleton':
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton
