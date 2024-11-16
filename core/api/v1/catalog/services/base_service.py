from abc import ABC

from core.api.v1.catalog.storages import (
    CategoryRepository,
    DocumentRepository,
    MaterialRepository,
)


class ServiceBase(ABC):
    pass


class MaterialServiceBase(ServiceBase):
    def __init__(self, repository=None):
        self.repository = repository or MaterialRepository()


class CategoryServiceBase(ServiceBase):
    def __init__(self, repository=None):
        self.repository = repository or CategoryRepository()


class DocumentServiceBase(ServiceBase):
    def __init__(self, repository=None):
        self.repository = repository or DocumentRepository()
