
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
    lat = serializers.SerializerMethodField()
    long = serializers.SerializerMethodField()

    class Meta:
        model = General
        fields = [
            'id', 'name', 'image', 'address', 'open_time', 'close_time',
            'tier', 'star_rating', 'delivery_available',
            'region', 'city', 'kalinka_filter', 'park_filter', 'rest_filter',
            'is_open_now', 'lat', 'long'
        ]
        depth = 1

    def get_is_open_now(self, obj):
        current_time = localtime(now()).time()
        if obj.open_time is None or obj.close_time is None:
            return False
        return obj.open_time <= current_time <= obj.close_time

    def get_lat(self, obj):
        return obj.helper.lat if hasattr(obj, 'helper') and obj.helper else None

    def get_long(self, obj):
        return obj.helper.long if hasattr(obj, 'helper') and obj.helper else None


class HelperSerializer(serializers.ModelSerializer):
    images = GeneralimageSerializer(many=True, read_only=True)
    # Shu yerda General'dan ma'lumotlarni olib kelamiz
    name = serializers.CharField(source='general.name', read_only=True)
    address = serializers.CharField(source='general.address', read_only=True)
    open_time = serializers.TimeField(source='general.open_time', read_only=True)
    close_time = serializers.TimeField(source='general.close_time', read_only=True)

    class Meta:
        model = Helper
        fields = [
            'id', 'general', 'phone', 'lat', 'long', 'description',
            'images', 'name', 'address', 'open_time', 'close_time'
        ]

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




