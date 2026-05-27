from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)

    brand = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    # preços
    price = models.DecimalField(max_digits=10, decimal_places=2)  # preço base
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # promo

    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    # imagem principal (vitrine)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_on_sale(self):
        return bool(self.sale_price) and self.sale_price < self.price

    @property
    def final_price(self):
        return self.sale_price if self.is_on_sale else self.price

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"GalleryImage #{self.id} - product={self.product_id}"


class ProductAttribute(models.Model):
    """
    Atributos dinâmicos estilo e-commerce:
    Ex: Material=Acetato, Cor=Preto, Lente=Polarizada, Tamanho=54-18-140 etc.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=80)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (
            "product",
            "name",
        )  # evita repetir "Cor" duas vezes no mesmo produto

    def __str__(self):
        return f"{self.name}: {self.value}"
