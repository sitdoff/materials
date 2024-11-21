import os
from datetime import datetime

from core.project.settings.local import DOCUMENT_NAME_TIME_FORMAT, DOCUMENT_ROOT

from .base_storage import DocumentRepositoryBase


class DocumentRepository(DocumentRepositoryBase):
    def get_by_id(self, target_id: int):
        try:
            document = self.model.objects.get(pk=target_id)
            return document
        except self.model.DoesNotExist as e:
            raise e

    def save_file(self, file_object):
        os.makedirs(DOCUMENT_ROOT, exist_ok=True)
        file_name = f"{datetime.now().strftime(DOCUMENT_NAME_TIME_FORMAT)}_{file_object.name}"
        file_path = os.path.join(DOCUMENT_ROOT, file_name)

        with open(file_path, "wb+") as file:
            for chunk in file_object.chunks():
                file.write(chunk)

        return {"title": file_name, "file_path": file_path}

    def create(
        self,
        title: str,
        file_path,
    ):
        serializer = self.serializer(
            data={
                "title": title,
                "file_path": file_path,
            }
        )
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        return document

    def list(self):
        return self.model.objects.all()

    def update_by_id(self, target_id, data):
        pass

    def delete(self, target_id):
        pass
