from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.urls import reverse

from .base_use_case import DocumentUseCaseBase


class UploadDocumentUseCase(DocumentUseCaseBase):
    def execute(self, file):
        try:
            document = self.service.save_document(file)
            serialized_document = self.serializer(instance=document).data
            serialized_document["check_status"] = reverse(
                "api:v1:catalog:documents:check-status", kwargs={"document_id": serialized_document["id"]}
            )
            return serialized_document
        except ValidationError as e:
            raise e


class CheckDocumentStatusUseCase(DocumentUseCaseBase):
    def execute(self, document_id):
        try:
            document = self.service.repository.get_document(document_id)
            serialized_document = self.serializer(instance=document).data
            return serialized_document
        except ObjectDoesNotExist as e:
            raise e
