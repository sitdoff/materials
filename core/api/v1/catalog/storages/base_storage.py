from abc import ABC, abstractmethod

from core.apps.catalog.models import CategoryModel, DocumentModel, MaterialModel
from core.apps.catalog.serializers import (
    CategorySerializer,
    DocumentSerializer,
    MaterialSerializer,
)


class StorageBase(ABC):

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def list(self, filters):
        pass

    @abstractmethod
    def get_by_id(self, target_id):
        pass

    @abstractmethod
    def update_by_id(self, target_id, data):
        pass

    @abstractmethod
    def delete(self, target_id):
        pass


class MaterialRepositoryBase(StorageBase):
    def __init__(self):
        self.model = MaterialModel
        self.serializer = MaterialSerializer


class CategoryRepositoryBase(StorageBase):
    def __init__(self) -> None:
        self.model = CategoryModel
        self.serializer = CategorySerializer


class DocumentRepositoryBase(StorageBase):
    def __init__(self) -> None:
        self.model = DocumentModel
        self.serializer = DocumentSerializer
