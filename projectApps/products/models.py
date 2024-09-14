from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        return self.name


class TypeAttribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AttributeDefinition(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(TypeAttribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class AttributeValue(models.Model):
    value = models.CharField(max_length=255)
    attribute_definition = models.ForeignKey(
        AttributeDefinition, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.attribute_definition.name}: {self.value}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    attributes = models.ManyToManyField(AttributeValue)

    def __str__(self):
        return self.name
