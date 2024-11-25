from django.db import models

from core.apps.common.models import TimedBaseModel


class DocumentModel(TimedBaseModel):
    class Status(models.TextChoices):
        NOT_PROCESSED = "not_processed", "Не обработан"
        PROCESSING = "processing", "Обрабатывается"
        SUCCESS = "success", "Успешно обработан"
        ERROR = "error", "Ошибка обработки"

    file = models.FileField(upload_to="uploads/", verbose_name="Файл документа")
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PROCESSING,
        verbose_name="Статус обработки",
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
