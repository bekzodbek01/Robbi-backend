
from .models import General, MenuCategory, MenuItem, GeneralImage
from rest_framework import serializers
from .models import Region, City, Category, ParkFilter, KalinkaFilter, RestaurantFilter, Helper
from datetime import datetime
from django.utils.timezone import localtime, now
import django_filters


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'icon_background_color', 'icon_background_color_night',
                  'Ln_background_color', 'Ln_background_color_night']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class RegionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'title',]


class RegionSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'title', 'cities']


class GeneralimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralImage
        fields = ['id', 'image']


class GeneralSerializer(serializers.ModelSerializer):
    is_open_now = serializers.SerializerMethodField()

    class Meta:
        model = General
        fields = [
            'id', 'name', 'image', 'address', 'open_time', 'close_time',
            'tier', 'star_rating', 'delivery_available', 'region', 'city', 'is_open_now',
        ]
        depth = 1

    def get_is_open_now(self, obj):
        current_time = localtime(now()).time()

        if obj.open_time is None or obj.close_time is None:
            return False  # Yoki `return None`, agar siz noaniqlikni ko‘rsatmoqchi bo‘lsangiz

        return obj.open_time <= current_time <= obj.close_time


class HelperSerializer(serializers.ModelSerializer):
    images = GeneralimageSerializer(many=True, read_only=True)

    class Meta:
        model = Helper
        fields = ['id', 'general', 'phone', 'lat', 'long', 'description', 'images']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'image']


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'items']


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




