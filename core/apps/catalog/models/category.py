from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class CategoryModel(MPTTModel):
    title = models.CharField(max_length=255, unique=True, verbose_name="Наименование категории")
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Родительская категория",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f'Категория "{self.title}"'
