from django.contrib import admin
from .models import (City, Region, Category, General, GeneralImage, MenuCategory, MenuItem, RestaurantFilter,
                     KalinkaFilter, ParkFilter, Helper)


class CityInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    inlines = [CityInline]


class GeneralImageAdmin(admin.TabularInline):
    model = GeneralImage
    list_display = ['id', 'general', 'image']


class HelperInline(admin.StackedInline):
    model = Helper
    extra = 0  # Yangi bo'sh form qo‘shilmaydi avtomatik
    max_num = 1


@admin.register(General)
class GeneralAdmin(admin.ModelAdmin):
    list_display = [
              'id', 'category', 'name', 'address', 'open_time', 'close_time', 'tier', 'star_rating',

        ]
    fields = ['category', 'name', 'image', 'address', 'region', 'city',
              'kalinka_filter', 'park_filter', 'rest_filter',
              'open_time', 'close_time', 'tier', 'star_rating', 'delivery_available',]
    inlines = [HelperInline, GeneralImageAdmin]

    filter_horizontal = ('rest_filter',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'icon_background_color', 'icon_background_color_night',
                    'Ln_background_color', 'Ln_background_color_night']


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'general', 'category', 'name', 'price', 'image']


admin.site.register(City)
admin.site.register(RestaurantFilter)
admin.site.register(KalinkaFilter)
admin.site.register(ParkFilter)