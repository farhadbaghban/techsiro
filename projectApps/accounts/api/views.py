import logging
from django.db import transaction
from django.utils.timezone import now


from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from projectApps.accounts.models import User


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from projectApps.accounts.api import services
from projectApps.accounts.api.permissions import IsAuthenticatedAndOwner

logger = logging.getLogger(__name__)



class UserListApiView(APIView):
    permission_classes = [IsAuthenticatedAndOwner]

    class OutputUserListApiViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = "__all__"

    def get(self, request, *args, **kwargs):
        user_instance = request.user
        serializer = self.OutputUserListApiViewSerializer(user_instance)
        return Response(serializer.data, status=HTTP_200_OK)


class UserRegisterApiView(APIView):
    class UserRegisterInputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True, max_length=128)

    @swagger_auto_schema(
        request_body=UserRegisterInputSerializer,
        responses={
            HTTP_201_CREATED: openapi.Response(
                "User created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            HTTP_400_BAD_REQUEST: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.UserRegisterInputSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                try:
                    validated_data = serializer.validated_data
                    user = services.check_user_exist(validated_data=validated_data)
                    if user:
                        return Response(
                            {"error": "You registered Before"},
                            status=HTTP_400_BAD_REQUEST,
                        )
                    user = services.create_user(validated_data=validated_data)
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "message": "User created successfully.",
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                        },
                        status=HTTP_201_CREATED,
                    )
                except Exception as e:
                    logger.error(f"Error: {str(e)}")
                    return Response(
                        {"error": f"cannot_create_user. {str(e)}"},
                        status=HTTP_400_BAD_REQUEST,
                    )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserDeleteApiView(APIView):
    permission_classes = [IsAuthenticatedAndOwner]

    @swagger_auto_schema(
        operation_description="Delete a user account.",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="JWT token (format: Bearer <token>)",
                required=True,
            ),
        ],
        responses={
            HTTP_200_OK: "Your account deleted successfully.",
            HTTP_401_UNAUTHORIZED: "You are not authenticated.",
            HTTP_403_FORBIDDEN: "You are not allowed to perform this action.",
            HTTP_404_NOT_FOUND: "User not found.",
            HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal server error.",
                examples={
                    "application/json": {
                        "error": "Something went wrong. Please try again."
                    }
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            with transaction.atomic():
                user.is_active = False
                user.de_activate_date = now()
                user.save()
                return Response(
                    {"message": "Your account deleted successfully."},
                    status=HTTP_200_OK,
                )
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return Response(
                {"error": f"An error occurred while deleting the account: {str(e)}"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserLoginView(APIView):
    class InputUserLoginViewSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True, max_length=128)

    @swagger_auto_schema(
        request_body=InputUserLoginViewSerializer,
        responses={
            HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": InputUserLoginViewSerializer.errors,
                },
            ),
            HTTP_404_NOT_FOUND: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": "User not found",
                },
            ),
            HTTP_401_UNAUTHORIZED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": "Invalid credentials",
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputUserLoginViewSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            try:
                user = User.objects.get(email=email, is_active=True)
                if not user.check_password(password):
                    return Response(
                        {"error": "Invalid credentials"},
                        status=HTTP_401_UNAUTHORIZED,
                    )

                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    status=HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
