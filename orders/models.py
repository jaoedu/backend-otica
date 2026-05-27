from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("canceled", "Canceled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    address_label = models.CharField(max_length=60, default="")
    address_zipcode = models.CharField(max_length=20, default="")
    address_street = models.CharField(max_length=160, default="")
    address_number = models.CharField(max_length=30, default="")
    address_complement = models.CharField(max_length=120, blank=True, default="")
    address_neighborhood = models.CharField(max_length=120, default="")
    address_city = models.CharField(max_length=120, default="")
    address_state = models.CharField(max_length=2, default="")
    prescription_image = models.ImageField(
        upload_to="orders/prescriptions/",
        blank=True,
        null=True,
    )
    prescription_notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - user={self.user_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField(default=1)

    # congelamos o preço final na compra (regra real de e-commerce)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"product={self.product_id} x {self.quantity}"
