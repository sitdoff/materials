from django.db import models


class MaterialModel(models.Model):
    title = models.CharField(max_length=255, verbose_name="Наименование")
    # category
    code = models.CharField(max_length=255, unique=True, verbose_name="Код метериала")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость материала")

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        # TODO задать индексы

    def __str__(self) -> str:
        return f"Material: Category-{self.title}-{self.code}"
