import os
import tempfile

import boto3
import environ
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


def get_s3_data_from_env():
    env = environ.Env()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=env("S3_ACCESS_KEY"),
        aws_secret_access_key=env("S3_SECRET_KEY"),
        endpoint_url=env("MINIO_URL"),
    )

    bucket_name = env("S3_BUCKET")

    return s3, bucket_name


@shared_task
def import_materials_from_xls(document_id: int):
    s3, bucket_name = get_s3_data_from_env()

    document = DocumentModel.objects.get(pk=document_id)
    document.status = DocumentModel.Status.PROCESSING
    document.save()

    file_path = document.file.name

    response = s3.get_object(Bucket=bucket_name, Key=file_path)

    with tempfile.NamedTemporaryFile(delete=True, suffix=".xlsx") as tmp_file:
        tmp_file.write(response["Body"].read())
        tmp_file_path = tmp_file.name

        try:
            workbook = openpyxl.load_workbook(tmp_file_path)
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
