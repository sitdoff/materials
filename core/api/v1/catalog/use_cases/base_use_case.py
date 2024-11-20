from abc import ABC, abstractmethod

from core.api.v1.catalog.services import (
    CategoryService,
    DocumentService,
    MaterialService,
)
from core.apps.catalog.serializers import (
    CategorySerializer,
    DocumentSerializer,
    MaterialSerializer,
)


class UseCaseBase(ABC):
    @abstractmethod
    def execute(self):
        pass


class CategoryUseCaseBase(UseCaseBase):
    def __init__(self, service=None, serializer=None):
        self.service = service or CategoryService()
        self.serializer = serializer or CategorySerializer


class MaterialUseCaseBase(UseCaseBase):
    def __init__(self, service=None, serializer=None):
        self.service = service or MaterialService()
        self.serializer = serializer or MaterialSerializer


class DocumentUseCaseBase(UseCaseBase):
    def __init__(self, service=None, serializer=None):
        self.service = service or DocumentService()
        self.serializer = serializer or DocumentSerializer
