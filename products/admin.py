from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.utils.safestring import mark_safe
from .models import Product, TagProduct, Category, CategoryDetails


class PriceRangeFilter(SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('low', 'До 1000₽'),
            ('medium', '1000₽ – 5000₽'),
            ('high', 'Более 5000₽'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'low':
            return queryset.filter(price__lt=1000)
        elif value == 'medium':
            return queryset.filter(price__gte=1000, price__lte=5000)
        elif value == 'high':
            return queryset.filter(price__gt=5000)


class HasTagsFilter(SimpleListFilter):
    title = 'Наличие тегов'
    parameter_name = 'has_tags'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'С тегами'),
            ('no', 'Без тегов'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(tags__isnull=False).distinct()
        elif value == 'no':
            return queryset.filter(tags__isnull=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'is_published', 'brief_info',
                    'tags_count', 'product_image')
    list_display_links = ('id', 'title')
    list_editable = ('is_published', )
    list_per_page = 5
    ordering = ['title']
    actions = ['set_published', 'set_draft']
    search_fields = ['title']
    list_filter = ['is_published', PriceRangeFilter, HasTagsFilter]
    readonly_fields = ['slug', 'product_image']
    exclude = ['is_published']
    filter_horizontal = ['tags']

    @admin.display(description="Изображение")
    def product_image(self, product: Product):
        return mark_safe(f"<img src='{product.image.url}' width=50>")

    @admin.display(description="Краткое описание")
    def brief_info(self, product: Product):
        return f"Описание {len(product.content)} символов."

    @admin.display(description="Кол-во тегов")
    def tags_count(self, product: Product):
        return product.tags.count()

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Product.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано записей: {count}.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Product.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!",
                          messages.WARNING)


@admin.register(TagProduct)
class TagProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')


@admin.register(CategoryDetails)
class CategoryDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    list_display_links = ('id',)
