from abc import ABC

from core.apps.catalog.models import CategoryModel, DocumentModel, MaterialModel
from core.apps.catalog.serializers import (
    CategorySerializer,
    DocumentSerializer,
    MaterialSerializer,
)


class StorageBase(ABC):
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
