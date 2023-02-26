# 3rd party imports
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import views, response, exceptions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# system imports
from django.db import transaction

from . import services
from banking_app.authentications import CustomUserAuthentication
from .models import User, Account, Transaction
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    AccountSerializer,
    TransactionSerializer,
)

# sefvices imports
from banking_app.constants import CREDIT, DEBIT
from .services import TransactionService
from banking_app.exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidTransactionTypeError,
)


class UserListAPIView(APIView):
    """
    Endpoint for getting a list of all users.
    """

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class CreateUserAPIView(APIView):
    """
    Endpoint for a new user's information.
    """

    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_summary="Register a new user",
        responses={201: "Created", 400: "Bad Request"},
    )
    @transaction.atomic
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            serializer.instance = services.create_user(user_data=data)
        except Exception as e:
            raise APIException(str(e))

        return Response(data=serializer.data)


class LoginUserAPIView(views.APIView):
    """
    Endpoint for logging-in a user using email & password.
    """

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_summary="Login a user",
        responses={200: "Created", 403: "Bad Request"},
    )
    @transaction.atomic
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid credentials")

        token = services.create_token(user_id=user.id)

        response_data = {"message": "Logged in successfully"}
        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie("jwt", token, httponly=True, secure=True)

        return response


class LogoutUserAPIView(APIView):
    """
    Endpoint for logging-out the current user's information.
    This endpoint can only be used if the user is authenticated
    """

    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        response_obj = response.Response()
        response_obj.delete_cookie("jwt")
        response_obj.data = {"message": "Goodbye!"}

        return response_obj


class GetUserAPIView(APIView):
    """
    Endpoint for deleting the current user's information.
    This endpoint can only be used if the user is authenticated
    """

    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return response.Response(serializer.data)


class DeleteCurrentUserAPIView(views.APIView):
    """
    Endpoint for deleting the current user's information.
     This endpoint can only be used if the user is authenticated
    """

    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def delete(self, request):
        user_email = request.user.email

        services.delete_user(user_email)

        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Account deleted successfully"}

        return resp


class UpdateCurrentUserAPIView(APIView):
    """
    Endpoint for updating the current user's information.
     This endpoint can only be used if the user is authenticated
    """

    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        operation_summary="Update current user",
        responses={200: "OK", 400: "Bad Request", 403: "Forbidden"},
    )
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()

        return response.Response(serializer.data)


class AccountViewSet(ModelViewSet):
    authentication_classes = [
        CustomUserAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TransactionList(generics.ListCreateAPIView):
    """
    API endpoint for creating and listing transactions for a specific account.
    """

    authentication_classes = [
        CustomUserAuthentication,
    ]
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description"]

    def get_queryset(self):
        account_id = self.kwargs["id"]
        return Transaction.objects.filter(account__id=account_id).order_by(
            "-timestamp"
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        account_id = self.kwargs["id"]
        amount = request.data.get("amount")
        description = request.data.get("description")
        transaction_type = request.data.get("type")

        service = TransactionService()

        try:
            account = service.get_account_by_id(account_id)
        except AccountNotFoundError:
            return Response(
                {"message": "Account not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            transaction = service.create_transaction(
                account=account,
                amount=amount,
                description=description,
                transaction_type=transaction_type,
                ip_address=service.get_client_ip(request),
            )
        except InsufficientFundsError:
            return Response(
                {"message": "Insufficient funds"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidTransactionTypeError:
            return Response(
                {"message": "Invalid transaction type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(transaction)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TransactionDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
