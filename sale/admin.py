from django.contrib import admin
from sale.models import Sale, SaleProduct


class SaleProductInline(admin.StackedInline):
    model = SaleProduct
    readonly_fields = ('_commission_applied', 'total',)
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    model = Sale
    inlines = [SaleProductInline]
    readonly_fields = ('total',)


admin.site.register(Sale, SaleAdmin)
