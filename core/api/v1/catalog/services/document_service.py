from core.api.v1.catalog.tasks import import_materials_from_xls

from .base_service import DocumentServiceBase


class DocumentService(DocumentServiceBase):
    def save_document(self, data):
        document_data = self.repository.save_file(data)
        document = self.repository.save_file_in_db(**document_data)
        import_materials_from_xls.delay_on_commit(document.pk)
        return document

    def get_document(self, target_id):
        return self.repository.get_document(target_id)
