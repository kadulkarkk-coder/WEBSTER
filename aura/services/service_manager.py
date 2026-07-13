class ServiceManager:
    """
    Stores and provides shared services.
    """

    def __init__(self):

        self._services = {}

    def register(self, name: str, service):

        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered.")

        self._services[name] = service

    def get(self, name: str):

        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")

        return self._services[name]

    def exists(self, name: str):

        return name in self._services

    def remove(self, name: str):

        if self.exists(name):
            del self._services[name]

    def list_services(self):

        return list(self._services.keys())