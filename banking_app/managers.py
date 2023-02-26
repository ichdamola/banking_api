from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        password: str = None,
        is_staff=False,
        is_superuser=False,
    ):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        password: str,
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save()

        return user
