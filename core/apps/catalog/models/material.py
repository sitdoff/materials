from django.db import models

from .category import CategoryModel


class MaterialModel(models.Model):
    title = models.CharField(max_length=255, verbose_name="Наименование")
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name="Категория",
    )
    code = models.CharField(max_length=255, unique=True, verbose_name="Код метериала")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость материала")

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        indexes = [
            models.Index(fields=["price"], name="material_price_idx"),
        ]

    def __str__(self) -> str:
        return f"Material: Category-{self.title}-{self.code}"

    def clean(self) -> None:
        if self.category.get_children().exists():
            raise ValueError("Товар можно привязать только к нижней категории")
