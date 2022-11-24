from django.contrib import admin
from sale.models import Sale, SaleProduct


class SaleProductInline(admin.StackedInline):
    model = SaleProduct
    extra = 1


class SaleAdmin(admin.ModelAdmin):
    model = Sale
    inlines = [SaleProductInline]


admin.site.register(Sale, SaleAdmin)
