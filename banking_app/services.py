# 3rd party imports
import jwt
import requests

from rest_framework import status
from rest_framework.response import Response

# system imports
import time
import random
import dataclasses
import datetime
from django.conf import settings
from typing import Optional, TYPE_CHECKING
from decimal import Decimal


from banking_app import models
from .constants import *
from .exceptions import *

if TYPE_CHECKING:
    from .models import User, Account, Transaction


@dataclasses.dataclass
class UserData:
    first_name: str
    last_name: str
    phone_number: str
    email: str
    password: Optional[str] = None
    id: Optional[int] = None

    @classmethod
    def from_user(cls, user: "User") -> "UserData":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            email=user.email,
            id=user.id,
        )


def create_user(user_data: UserData) -> UserData:
    user = models.User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        email=user_data.email,
    )
    if user_data.password:
        user.set_password(user_data.password)
    user.save()
    return UserData.from_user(user)


def find_user_by_email(email: str) -> Optional["User"]:
    return User.objects.filter(email=email).first()


def create_token(user_id: int) -> str:
    payload = {
        "id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


def delete_user(user_email):
    try:
        user = models.User.objects.get(email=user_email)
    except models.User.DoesNotExist:
        # Return an error or raise an exception if user doesn't exist
        # For example:
        raise ValueError("User does not exist")

    # Delete the user object
    user.delete()

    # Optionally, return some data or a message indicating success
    return "User deleted successfully"


def generate_account_number():
    # Get current timestamp
    timestamp = int(time.time())
    # Generate random string of length 6
    rand_str = "".join(
        random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6)
    )
    # Combine timestamp and random string
    account_number = f"{timestamp}-{rand_str}"
    return account_number


class TransactionService:
    def get_account_by_id(self, account_id: int) -> "Account":
        try:
            return models.Account.objects.get(id=account_id)
        except models.Account.DoesNotExist:
            raise AccountNotFoundError

    def create_transaction(
        self,
        account: "Account",
        amount: Decimal,
        description: str,
        transaction_type: str,
        ip_address: str,
    ) -> "Transaction":
        if transaction_type == CREDIT:
            account.amount += amount
        elif transaction_type == DEBIT:
            if account.amount < amount:
                raise InsufficientFundsError
            account.amount -= amount
        else:
            raise InvalidTransactionTypeError

        account.save()

        return models.Transaction.objects.create(
            account=account,
            amount=amount,
            description=description,
            type=transaction_type,
            ip_address=ip_address,
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        if ip == "127.0.0.1" and settings.DEBUG:
            ip = requests.get("https://api.ipify.org").text
        return ip
