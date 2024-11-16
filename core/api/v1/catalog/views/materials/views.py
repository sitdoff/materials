from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.v1.catalog.use_cases import (
    CreateMaterialUseCase,
    DeleteMaterialUseCase,
    ListMateriasUseCase,
    RetrieveByCodeMaterialUseCase,
    RetrieveByIdMaterialUseCase,
    UpdateByCodeMaterialUseCase,
    UpdateByIdMaterialUseCase,
)


class MaterialListCreateView(APIView):
    def get(self, request: Request):
        use_case = ListMateriasUseCase()
        filters = request.query_params
        materals = use_case.execute(filters=filters)
        return Response(data=materals, status=status.HTTP_200_OK)

    def post(self, request: Request):
        use_case = CreateMaterialUseCase()
        try:
            material = use_case.execute(data=request.data)
            return Response(data=material, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MaterialDetailByIdView(APIView):
    def get(self, request: Request, material_id: int):
        use_case = RetrieveByIdMaterialUseCase()
        try:
            material = use_case.execute(target_id=material_id)
            return Response(data=material, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, material_id: int):
        use_case = UpdateByIdMaterialUseCase()
        try:
            material = use_case.execute(
                target_id=material_id,
                data=request.data,
            )
            return Response(data=material, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class MaterialDetailByCode(APIView):
    def get(self, request: Request, material_code: str):
        use_case = RetrieveByCodeMaterialUseCase()
        try:
            material = use_case.execute(material_code)
            return Response(data=material, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, material_code: str):
        use_case = UpdateByCodeMaterialUseCase()
        try:
            material = use_case.execute(target_code=material_code, data=request.data)
            return Response(data=material, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class MaterialDeleteView(APIView):
    def delete(self, request: Request, material_id: int):
        use_case = DeleteMaterialUseCase()
        try:
            use_case.execute(target_id=material_id)
            return Response(
                data={"success": f"Matereal with ID {material_id} was deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
