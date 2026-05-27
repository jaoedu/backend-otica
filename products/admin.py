from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "brand",
        "category",
        "price",
        "sale_price",
        "stock",
        "active",
    )
    list_filter = ("active", "category", "brand")
    search_fields = ("name", "description", "brand")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductAttributeInline]
