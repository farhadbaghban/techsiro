from typing import Optional
from projectApps.accounts.models import User


def create_user(validated_data) -> User:
    email = validated_data.get("email")
    user = User.objects.create(
        email=email,
    )
    # Set and hash the password
    user.set_password(validated_data["password"])
    user.save()
    return user


def check_user_exist(validated_data) -> Optional[User]:
    email = validated_data.get("email")
    user = User.objects.filter(email=email)
    if user:
        return user.first()
    else:
        return None
