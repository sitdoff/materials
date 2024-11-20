from core.api.v1.catalog.tasks import import_materials_from_xls

from .base_service import DocumentServiceBase


class DocumentService(DocumentServiceBase):
    def upload_document(self, data):
        document_data = self.repository.save_file(data)
        return document_data

    def save(self, data):
        document = self.repository.save_file_in_db(**data)
        return document

    def run_task(self, document_id):
        import_materials_from_xls.delay_on_commit(document_id)

    def get_document(self, target_id):
        return self.repository.get_document(target_id)
