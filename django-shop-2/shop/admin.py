from django.contrib import admin
from .models import Category, Product, Edition, Contact, Review, Size, Variants

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}

class ProductVariantInline(admin.TabularInline):
    model = Variants
    extra = 1
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'updated')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]

@admin.register(Edition)
class EditionADmin(admin.ModelAdmin):
    list_display = ('edition', 'slug',)
    prepopulated_fields = {'slug': ('edition',)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email','message')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email','review_text')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    prepopulated_fields = {'code': ('name',)}
