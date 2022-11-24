from django.contrib import admin
from product.models import Product, ProductCommissionSchedule


class ProductCommissionScheduleInline(admin.StackedInline):
    model = ProductCommissionSchedule
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductCommissionScheduleInline]


admin.site.register(Product, ProductAdmin)
