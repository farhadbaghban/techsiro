from datetime import datetime
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(is_active=True)

    def delete(self):
        self.update(is_active=False, de_activate_date=datetime.date)
        return super().delete()


class DeletedUserManager(BaseUserManager):
    def get_queryset(self):
        return super(DeletedUserManager, self).get_queryset().filter(is_active=False)
