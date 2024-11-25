from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from core.apps.catalog.serializers import DocumentSerializer

from .base_storage import DocumentRepositoryBase


class DocumentRepository(DocumentRepositoryBase):
    def get_by_id(self, target_id: int):
        try:
            document = self.model.objects.get(pk=target_id)
            return document
        except ObjectDoesNotExist as e:
            raise e

    def create(self, data):
        print(data)
        file_name = f"{datetime.now().strftime(settings.UPLOAD_FILE_NAME_TIME_FORMAT)}_{data['file'].name}"
        data["file"].name = file_name
        serializer = DocumentSerializer(data=data)
        try:
            if serializer.is_valid():
                document = serializer.save()  # Файл загружается в S3
                return document
        except ValidationError as e:
            raise e

    def list(self):
        return self.model.objects.all()

    def update_by_id(self, target_id, data):
        pass

    def delete(self, target_id):
        pass
