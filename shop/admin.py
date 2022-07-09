from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    prepopulated_fields = {'slug': ('name',)}


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="100"')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    actions = ('publish', 'unpublish')
    inlines = (ProductImagesInline,)
    prepopulated_fields = {'slug': ('brand', 'vendor_code')}

    def publish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(available=True)
        if row_update == 1:
            message_bit = "1 entry has been updated"
        else:
            message_bit = f"{row_update} entries has been updated"
        self.message_user(request, f"{message_bit}")

    def unpublish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(available=False)
        if row_update == 1:
            message_bit = "1 entry has been updated"
        else:
            message_bit = f"{row_update} entries has been updated"
        self.message_user(request, f"{message_bit}")


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'image_tag')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'color_bg')


admin.site.register(Banner)
admin.site.register(Size)
admin.site.register(Comment)
