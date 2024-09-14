from django.db import models
from django.conf import settings
from projectApps.products.models import Product


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comment_response",
    )
    is_response = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.product.name}"
