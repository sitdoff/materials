from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from core.apps.catalog.models import CategoryModel, DocumentModel, MaterialModel


@admin.register(MaterialModel)
class MaterialModelAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "price")


@admin.register(CategoryModel)
class CategoryModelAdmin(MPTTModelAdmin):
    list_display = ("title",)


@admin.register(DocumentModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ("title", "file_path", "status", "created_at")
