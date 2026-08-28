from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
        return self.children.all()

    def is_root(self):
        return self.parent_id is None

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.id])


class Product(models.Model):
    name = models.CharField("назва", max_length=100)

    category = models.ForeignKey(
        Category,
        verbose_name="категорія",
        on_delete=models.PROTECT,
        related_name="products",
    )

    price = models.DecimalField("ціна", decimal_places=2, max_digits=10)

    stock = models.PositiveIntegerField("залишок на складі", default=0)

    slug = models.SlugField("slug", unique=True, blank=True)

    is_featured = models.BooleanField("хіт продажів", default=False)

    description = models.TextField("опис", blank=True, default="")

    is_mysterious = models.BooleanField("загадковий товар", default=False)

    rarity = models.CharField(
        "рідкісність",
        max_length=20,
        choices=[
            ('common', 'Звичайний'),
            ('rare', 'Рідкісний'),
            ('epic', 'Епічний'),
            ('legend', 'Легендарний'),
            ('mythic', 'Міфічний'),
            ('divine', 'Божественний'),
        ],
        default='common',
    )

    created_at = models.DateTimeField("дата створення", auto_now_add=True)
    modified_at = models.DateTimeField("дата зміни", auto_now=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товари"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=False)
            if not base_slug:
                base_slug = self._transliterate(self.name)

            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def _transliterate(self, text):
        table = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
            'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
            'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
            'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
            'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ь': '', 'ю': 'yu', 'я': 'ya',
        }
        result = []
        for char in text.lower():
            result.append(table.get(char, char if char.isalnum() else '-'))
        slug = ''.join(result).strip('-')
        while '--' in slug:
            slug = slug.replace('--', '-')
        return slug or 'product'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


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
