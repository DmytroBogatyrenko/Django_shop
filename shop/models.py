from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("назва", max_length=100)

    parent = models.ForeignKey(
        "self",
        verbose_name="батьківська категорія",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    class Meta:
        verbose_name = "категорія"
        verbose_name_plural = "категорії"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_children(self):
        """Повертає прямих нащадків цієї категорії (підкатегорії)."""
        return self.children.all()

    def is_root(self):
        """Чи є категорія кореневою (без батька)."""
        return self.parent_id is None


class Product(models.Model):
    name = models.CharField("назва", max_length=100)

    category = models.ForeignKey(
        Category,
        verbose_name="категорія",
        on_delete=models.PROTECT,
        related_name="products",
    )

    price = models.DecimalField("ціна", decimal_places=2, max_digits=10)

    slug = models.SlugField("slug", unique=True)

    created_at = models.DateTimeField("дата створення", auto_now_add=True)

    modified_at = models.DateTimeField("дата зміни", auto_now=True)

    def get_absolute_url(self):
            # Потрібно передавати І id, І slug:
            return reverse('shop:product_detail', args=[self.id, self.slug])
    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товари"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="товар",
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        "зображення",
        upload_to="products/%Y/%m/%d/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        help_text="Дозволені формати: JPG, JPEG, PNG, WebP",
    )

    class Meta:
        verbose_name = "зображення товару"
        verbose_name_plural = "зображення товарів"

    def __str__(self):
        return f"Фото для {self.product.name}"