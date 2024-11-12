from django.contrib import admin

from core.apps.catalog.models import MaterialModel


# Register your models here.
@admin.register(MaterialModel)
class MaterialModelAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "price")
