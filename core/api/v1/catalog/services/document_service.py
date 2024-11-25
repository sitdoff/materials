from core.api.v1.catalog.tasks import import_materials_from_xls

from .base_service import DocumentServiceBase


class DocumentService(DocumentServiceBase):

    def save(self, data):
        document = self.repository.create(data)
        return document

    # def run_task(self, document_id):
    #     import_materials_from_xls.delay_on_commit(document_id)
    #
    def get_document(self, target_id):
        return self.repository.get_by_id(target_id)
