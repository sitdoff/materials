import openpyxl
from celery import shared_task
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from core.apps.catalog.models import DocumentModel, MaterialModel
from core.apps.catalog.serializers import MaterialSerializer


def get_data_from_sheet(sheet):
    materials_data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        title, category_name, category_id, code, price = row
        data = {
            "title": title,
            "category": category_id,
            "code": code,
            "price": price,
        }
        materials_data.append(data)
    return materials_data


def get_valid_materials(materials_data):
    valid_materials = []
    for material_data in materials_data:
        serializer = MaterialSerializer(data=material_data)
        try:
            if serializer.is_valid(raise_exception=True):
                valid_materials.append(MaterialModel(**serializer.validated_data))
        except ValidationError as e:
            raise ValidationError(
                {
                    "error": str(e),
                    "data": material_data,
                }
            )
    return valid_materials


@shared_task
def import_materials_from_xls(document_id: int):
    document = DocumentModel.objects.get(pk=document_id)
    file_path = document.file_path
    document.status = DocumentModel.Status.PROCESSING
    document.save()

    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    except FileNotFoundError as e:
        document.status = DocumentModel.Status.ERROR
        document.save()
        raise e

    try:
        materials_data = get_data_from_sheet(sheet)
    except Exception as e:
        document.status = DocumentModel.Status.ERROR
        document.save()
        raise e

    try:
        with transaction.atomic():
            valid_materials = get_valid_materials(materials_data)
            MaterialModel.objects.bulk_create(valid_materials)
    except (ValidationError, IntegrityError) as e:
        document.status = DocumentModel.Status.ERROR
        document.save()
        raise e

    document.status = DocumentModel.Status.SUCCESS
    document.save()
