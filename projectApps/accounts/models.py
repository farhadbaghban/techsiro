from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from projectApps.accounts.managers import UserManager, DeletedUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    de_activate_date = models.DateTimeField(blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "userss"

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
        return super().delete(using, keep_parents)

    @property
    def is_staff(self):
        return self.is_admin


class DeletedUsers(User):
    objects = DeletedUserManager()

    class Meta:
        proxy = True
