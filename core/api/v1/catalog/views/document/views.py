from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.v1.catalog.use_cases import (
    CheckDocumentStatusUseCase,
    UploadDocumentUseCase,
)


class DocumentUploadView(APIView):
    def post(self, request: Response):
        use_case = UploadDocumentUseCase()
        file = request.FILES["file"]
        try:
            document_data = use_case.execute(file)
            return Response(data=document_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DocumentCheckStatus(APIView):
    def get(self, request: Request, document_id: int):
        use_case = CheckDocumentStatusUseCase()
        try:
            document = use_case.execute(document_id)
            return Response(data=document, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
