
from .models import General, MenuCategory, MenuItem, GeneralImage
from rest_framework import serializers
from .models import Region, City, Category, ParkFilter, KalinkaFilter, RestaurantFilter
from datetime import datetime
from django.utils.timezone import localtime, now
import django_filters


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class RegionSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'title', 'cities']


class RegionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'title',]


class GeneralimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralImage
        fields = ['id', 'image']


class RestaurantFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFilter
        fields = ['id', 'name']


class KalinkaFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KalinkaFilter
        fields = ['id', 'name']


class ParkFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkFilter
        fields = ['id', 'name']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'image']


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'items']


class GeneralSerializer(serializers.ModelSerializer):
    images = GeneralimageSerializer(many=True, read_only=True)
    menu_categories = serializers.SerializerMethodField()
    is_open_now = serializers.SerializerMethodField()

    class Meta:
        model = General
        fields = [
            'id', 'name', 'image', 'address', 'phone', 'lat', 'long',
            'description', 'open_time', 'close_time',  # ✅ TO‘G‘RI
            'tier', 'star_rating', 'delivery_available',
            'region', 'city', 'images', 'menu_categories',
            'is_open_now'  # ✅ Dynamic field
        ]
        depth = 1

    def get_menu_categories(self, obj):
        categories = MenuCategory.objects.filter(items__general=obj).distinct()
        return MenuCategorySerializer(categories, many=True).data

    def get_is_open_now(self, obj):
        current_time = localtime(now()).time()

        if obj.open_time is None or obj.close_time is None:
            return False  # Yoki `return None`, agar siz noaniqlikni ko‘rsatmoqchi bo‘lsangiz

        return obj.open_time <= current_time <= obj.close_time


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'icon_background_color', 'icon_background_color_night',
                  'Ln_background_color', 'Ln_background_color_night']
