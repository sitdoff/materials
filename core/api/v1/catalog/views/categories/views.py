from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.v1.catalog.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    ListCategoriesUseCase,
    RetrieveByIdCategoryUseCase,
    TreeCategoriesUseCase,
    UpdateByIdCategoryUseCase,
)


class CategoryListCreateView(APIView):
    def get(self, request: Request):
        filters = request.query_params.dict()
        use_case = ListCategoriesUseCase()
        categories = use_case.execute(filters=filters)
        return Response(data=categories, status=status.HTTP_200_OK)

    def post(self, request: Request):
        use_case = CreateCategoryUseCase()
        try:
            category = use_case.execute(data=request.data)
            return Response(data=category, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CategoryTreeCreateView(APIView):
    def get(self, request: Request):
        use_case = TreeCategoriesUseCase()
        categories = use_case.execute()
        return Response(data=categories, status=status.HTTP_200_OK)


class CategoryDetailByIdView(APIView):
    def get(self, request: Request, category_id: int):
        use_case = RetrieveByIdCategoryUseCase()
        try:
            category = use_case.execute(target_id=category_id)
            return Response(data=category, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request: Request, category_id: int):
        use_case = UpdateByIdCategoryUseCase()
        try:
            category = use_case.execute(category_id, request.data)
            return Response(data=category, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class CategoryDeleteView(APIView):
    def delete(self, request: Request, category_id: int):
        use_case = DeleteCategoryUseCase()
        try:
            use_case.execute(category_id)
            return Response(
                data={"success": f"Category with ID {category_id} was deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ObjectDoesNotExist as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ProtectedError as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_423_LOCKED,
            )
