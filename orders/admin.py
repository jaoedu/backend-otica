from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "address_label",
        "address_city",
        "created_at",
    )
    list_filter = ("status", "address_state", "created_at")
    search_fields = ("user__email", "address_label", "address_street", "address_city")
    readonly_fields = (
        "user",
        "created_at",
        "address_label",
        "address_zipcode",
        "address_street",
        "address_number",
        "address_complement",
        "address_neighborhood",
        "address_city",
        "address_state",
        "prescription_image",
        "prescription_notes",
    )
    inlines = [OrderItemInline]
